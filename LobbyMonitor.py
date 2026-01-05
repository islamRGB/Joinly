import sys
import requests
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QLineEdit, QDialog)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *
import math

class Lobby3DView(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.rotation = 0
        self.players = []
        self.bots = []
        self.current_player_id = None
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_rotation)
        self.timer.start(16)
    
    def update_rotation(self):
        self.rotation += 0.5
        self.update()
    
    def set_entities(self, players, bots, current_player_id):
        self.players = players
        self.bots = bots
        self.current_player_id = current_player_id
        self.update()
    
    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        glLightfv(GL_LIGHT0, GL_POSITION, [5, 5, 5, 1])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1])
        
        glClearColor(0.1, 0.13, 0.18, 1.0)
    
    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h if h != 0 else 1, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
    
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        gluLookAt(0, 8, 15, 0, 0, 0, 0, 1, 0)
        
        self.draw_floor()
        
        all_entities = []
        for player in self.players:
            all_entities.append({'data': player, 'is_bot': False})
        for bot in self.bots:
            all_entities.append({'data': bot, 'is_bot': True})
        
        total_entities = len(all_entities)
        if total_entities > 0:
            radius = max(3, total_entities * 0.5)
            
            for i, entity in enumerate(all_entities):
                angle = (360 / total_entities) * i + self.rotation
                x = radius * math.cos(math.radians(angle))
                z = radius * math.sin(math.radians(angle))
                
                is_current = entity['data'].get('player_id') == self.current_player_id
                is_ready = entity['data'].get('ready', False)
                is_bot = entity['is_bot']
                
                self.draw_player_cube(x, 0, z, is_current, is_ready, is_bot)
                
                glDisable(GL_LIGHTING)
                self.render_text_3d(x, 2.5, z, entity['data'].get('username', 'Unknown'))
                glEnable(GL_LIGHTING)
    
    def draw_floor(self):
        glDisable(GL_LIGHTING)
        glColor3f(0.15, 0.2, 0.25)
        glBegin(GL_QUADS)
        size = 20
        glVertex3f(-size, -0.1, -size)
        glVertex3f(size, -0.1, -size)
        glVertex3f(size, -0.1, size)
        glVertex3f(-size, -0.1, size)
        glEnd()
        
        glColor3f(0.2, 0.25, 0.3)
        glBegin(GL_LINES)
        for i in range(-10, 11):
            glVertex3f(i, -0.09, -10)
            glVertex3f(i, -0.09, 10)
            glVertex3f(-10, -0.09, i)
            glVertex3f(10, -0.09, i)
        glEnd()
        glEnable(GL_LIGHTING)
    
    def draw_player_cube(self, x, y, z, is_current, is_ready, is_bot):
        glPushMatrix()
        glTranslatef(x, y + 1, z)
        
        bounce = abs(math.sin(self.rotation * 0.05)) * 0.3 if is_ready else 0
        glTranslatef(0, bounce, 0)
        
        glRotatef(self.rotation * 2, 0, 1, 0)
        
        if is_current:
            glColor3f(1.0, 0.84, 0.0)
        elif is_ready:
            glColor3f(0.15, 0.68, 0.38)
        elif is_bot:
            glColor3f(0.95, 0.61, 0.07)
        else:
            glColor3f(0.31, 0.78, 0.97)
        
        size = 1.2 if is_current else 1.0
        
        glBegin(GL_QUADS)
        
        glVertex3f(-size, -size, size)
        glVertex3f(size, -size, size)
        glVertex3f(size, size, size)
        glVertex3f(-size, size, size)
        
        glVertex3f(-size, -size, -size)
        glVertex3f(-size, size, -size)
        glVertex3f(size, size, -size)
        glVertex3f(size, -size, -size)
        
        glVertex3f(-size, size, -size)
        glVertex3f(-size, size, size)
        glVertex3f(size, size, size)
        glVertex3f(size, size, -size)
        
        glVertex3f(-size, -size, -size)
        glVertex3f(size, -size, -size)
        glVertex3f(size, -size, size)
        glVertex3f(-size, -size, size)
        
        glVertex3f(size, -size, -size)
        glVertex3f(size, size, -size)
        glVertex3f(size, size, size)
        glVertex3f(size, -size, size)
        
        glVertex3f(-size, -size, -size)
        glVertex3f(-size, -size, size)
        glVertex3f(-size, size, size)
        glVertex3f(-size, size, -size)
        
        glEnd()
        
        glPopMatrix()
    
    def render_text_3d(self, x, y, z, text):
        pass

class JoinDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Join Lobby')
        self.setFixedSize(400, 200)
        self.setStyleSheet('background: #16213E; color: white;')
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel('Join Lobby')
        title.setStyleSheet('font-size: 24px; font-weight: bold; color: #4FC3F7;')
        layout.addWidget(title)
        
        self.lobby_input = QLineEdit()
        self.lobby_input.setPlaceholderText('Enter Lobby ID')
        self.lobby_input.setStyleSheet('''
            QLineEdit {
                background: #0F3460;
                border: 2px solid #1E5F8C;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: white;
            }
        ''')
        layout.addWidget(self.lobby_input)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter Your Username')
        self.username_input.setStyleSheet('''
            QLineEdit {
                background: #0F3460;
                border: 2px solid #1E5F8C;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: white;
            }
        ''')
        layout.addWidget(self.username_input)
        
        btn_layout = QHBoxLayout()
        
        join_btn = QPushButton('Join')
        join_btn.setFixedHeight(40)
        join_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        join_btn.setStyleSheet('''
            QPushButton {
                background: #27AE60;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #229954;
            }
        ''')
        join_btn.clicked.connect(self.accept)
        btn_layout.addWidget(join_btn)
        
        cancel_btn = QPushButton('Cancel')
        cancel_btn.setFixedHeight(40)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet('''
            QPushButton {
                background: #546E7A;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #455A64;
            }
        ''')
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)

class LobbyMonitor3D(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_url = 'http://localhost:5000/api'
        self.current_lobby_id = None
        self.current_player_id = None
        self.init_ui()
        self.show_join_dialog()
    
    def init_ui(self):
        self.setWindowTitle('Joinly - 3D Lobby Monitor')
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet('background: #1A1A2E;')
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        header = QWidget()
        header.setFixedHeight(80)
        header.setStyleSheet('background: #0F3460;')
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        title = QLabel('🎮 JOINLY 3D LOBBY')
        title.setStyleSheet('color: #4FC3F7; font-size: 28px; font-weight: bold;')
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.lobby_label = QLabel('Not in lobby')
        self.lobby_label.setStyleSheet('color: white; font-size: 16px;')
        header_layout.addWidget(self.lobby_label)
        
        self.ready_btn = QPushButton('Ready Up')
        self.ready_btn.setFixedSize(120, 40)
        self.ready_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ready_btn.setStyleSheet('''
            QPushButton {
                background: #27AE60;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #229954;
            }
        ''')
        self.ready_btn.clicked.connect(self.toggle_ready)
        self.ready_btn.setEnabled(False)
        header_layout.addWidget(self.ready_btn)
        
        leave_btn = QPushButton('Leave')
        leave_btn.setFixedSize(100, 40)
        leave_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        leave_btn.setStyleSheet('''
            QPushButton {
                background: #E74C3C;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #C0392B;
            }
        ''')
        leave_btn.clicked.connect(self.leave_lobby)
        header_layout.addWidget(leave_btn)
        
        main_layout.addWidget(header)
        
        self.gl_widget = Lobby3DView()
        main_layout.addWidget(self.gl_widget)
        
        footer = QWidget()
        footer.setFixedHeight(50)
        footer.setStyleSheet('background: #0F3460;')
        footer_layout = QHBoxLayout(footer)
        
        footer_label = QLabel('Made by <a href="https://emodi.me" style="color: #4FC3F7;">emodi</a> | 🟡 You = Gold Cube | 🟢 Ready = Green | 🔵 Players = Blue | 🟠 Bots = Orange')
        footer_label.setOpenExternalLinks(True)
        footer_label.setStyleSheet('color: #90A4AE; font-size: 12px;')
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_layout.addWidget(footer_label)
        
        main_layout.addWidget(footer)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_lobby)
        self.timer.start(2000)
    
    def show_join_dialog(self):
        dialog = JoinDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            lobby_id = dialog.lobby_input.text().strip()
            username = dialog.username_input.text().strip()
            
            if lobby_id and username:
                self.join_lobby(lobby_id, username)
            else:
                self.close()
        else:
            self.close()
    
    def join_lobby(self, lobby_id, username):
        try:
            self.current_player_id = f"player_{random.randint(10000, 99999)}"
            
            response = requests.post(
                f'{self.api_url}/lobbies/{lobby_id}/join',
                json={
                    'player_id': self.current_player_id,
                    'username': username,
                    'metadata': {}
                },
                timeout=2
            )
            
            if response.status_code == 200:
                self.current_lobby_id = lobby_id
                self.lobby_label.setText(f'Lobby: {lobby_id} | You: {username}')
                self.ready_btn.setEnabled(True)
                self.refresh_lobby()
            else:
                self.lobby_label.setText('Failed to join lobby')
        
        except Exception as e:
            self.lobby_label.setText(f'Error: {str(e)[:30]}')
    
    def toggle_ready(self):
        if not self.current_lobby_id or not self.current_player_id:
            return
        
        try:
            is_ready = self.ready_btn.text() == 'Ready Up'
            
            requests.post(
                f'{self.api_url}/lobbies/{self.current_lobby_id}/ready',
                json={
                    'player_id': self.current_player_id,
                    'ready': is_ready
                },
                timeout=2
            )
            
            if is_ready:
                self.ready_btn.setText('Not Ready')
                self.ready_btn.setStyleSheet('''
                    QPushButton {
                        background: #E74C3C;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 14px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background: #C0392B;
                    }
                ''')
            else:
                self.ready_btn.setText('Ready Up')
                self.ready_btn.setStyleSheet('''
                    QPushButton {
                        background: #27AE60;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 14px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background: #229954;
                    }
                ''')
            
            self.refresh_lobby()
        
        except Exception as e:
            print(f"Ready error: {e}")
    
    def leave_lobby(self):
        if self.current_lobby_id and self.current_player_id:
            try:
                requests.post(
                    f'{self.api_url}/lobbies/{self.current_lobby_id}/leave',
                    json={'player_id': self.current_player_id},
                    timeout=2
                )
            except:
                pass
        
        self.close()
    
    def refresh_lobby(self):
        if not self.current_lobby_id:
            return
        
        try:
            response = requests.get(f'{self.api_url}/lobbies/{self.current_lobby_id}', timeout=2)
            
            if response.status_code == 200:
                data = response.json()
                lobby = data.get('lobby', {})
                
                players = lobby.get('players', [])
                bots = lobby.get('bots', [])
                
                self.gl_widget.set_entities(players, bots, self.current_player_id)
        
        except:
            pass

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    monitor = LobbyMonitor3D()
    monitor.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
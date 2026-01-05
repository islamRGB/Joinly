import 'package:flutter/material.dart';
import 'core/joinly_client.dart';
import 'core/models.dart';
import 'screens/lobby_screen.dart';

void main() {
  runApp(JoinlyApp());
}

class JoinlyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Joinly',
      theme: ThemeData(
        primaryColor: Color(0xFF4FC3F7),
        scaffoldBackgroundColor: Color(0xFF1A1A2E),
      ),
      home: HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final client = JoinlyClient(baseUrl: 'http://localhost:5000');
  final usernameController = TextEditingController();
  final lobbyIdController = TextEditingController();
  List<Lobby> lobbies = [];
  
  @override
  void initState() {
    super.initState();
    loadLobbies();
  }
  
  Future<void> loadLobbies() async {
    try {
      final data = await client.getLobbies();
      setState(() {
        lobbies = data;
      });
    } catch (e) {
      print('Error loading lobbies: $e');
    }
  }
  
  Future<void> joinLobby() async {
    final username = usernameController.text;
    final lobbyId = lobbyIdController.text;
    
    if (username.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Please enter a username')),
      );
      return;
    }
    
    if (lobbyId.isEmpty) {
      await createAndJoin();
      return;
    }
    
    final playerId = 'player_${DateTime.now().millisecondsSinceEpoch}';
    
    try {
      await client.joinLobby(lobbyId, playerId, username);
      
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => LobbyScreen(
            client: client,
            lobbyId: lobbyId,
            playerId: playerId,
          ),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to join lobby: $e')),
      );
    }
  }
  
  Future<void> createAndJoin() async {
    final username = usernameController.text;
    final lobbyId = 'lobby_${DateTime.now().millisecondsSinceEpoch}';
    
    try {
      await client.createLobby(lobbyId, {});
      lobbyIdController.text = lobbyId;
      await joinLobby();
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to create lobby: $e')),
      );
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Joinly', style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: Color(0xFF0F3460),
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: loadLobbies,
          ),
        ],
      ),
      body: Padding(
        padding: EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Container(
              padding: EdgeInsets.all(30),
              decoration: BoxDecoration(
                color: Color(0xFF16213E),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text(
                    'Join a Lobby',
                    style: TextStyle(
                      color: Color(0xFF4FC3F7),
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: 20),
                  TextField(
                    controller: usernameController,
                    style: TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      hintText: 'Enter your username',
                      hintStyle: TextStyle(color: Colors.white54),
                      filled: true,
                      fillColor: Color(0xFF0F3460),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: BorderSide.none,
                      ),
                    ),
                  ),
                  SizedBox(height: 15),
                  TextField(
                    controller: lobbyIdController,
                    style: TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      hintText: 'Lobby ID (optional)',
                      hintStyle: TextStyle(color: Colors.white54),
                      filled: true,
                      fillColor: Color(0xFF0F3460),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: BorderSide.none,
                      ),
                    ),
                  ),
                  SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: joinLobby,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Color(0xFF4FC3F7),
                      padding: EdgeInsets.symmetric(vertical: 15),
                    ),
                    child: Text(
                      'Join Game',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                  ),
                  SizedBox(height: 10),
                  ElevatedButton(
                    onPressed: createAndJoin,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Color(0xFF27AE60),
                      padding: EdgeInsets.symmetric(vertical: 15),
                    ),
                    child: Text(
                      'Create New Lobby',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                  ),
                ],
              ),
            ),
            SizedBox(height: 30),
            Text(
              'Available Lobbies',
              style: TextStyle(
                color: Color(0xFF4FC3F7),
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 15),
            Expanded(
              child: ListView.builder(
                itemCount: lobbies.length,
                itemBuilder: (context, index) {
                  final lobby = lobbies[index];
                  return Card(
                    color: Color(0xFF16213E),
                    margin: EdgeInsets.only(bottom: 10),
                    child: ListTile(
                      title: Text(
                        lobby.lobbyId,
                        style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                      ),
                      subtitle: Text(
                        '${lobby.playerCount}/${lobby.maxPlayers} players',
                        style: TextStyle(color: Colors.white70),
                      ),
                      trailing: Container(
                        padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                        decoration: BoxDecoration(
                          color: lobby.state == 'ready' ? Color(0xFF27AE60) : Color(0xFFF39C12),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          lobby.state.toUpperCase(),
                          style: TextStyle(color: Colors.white, fontSize: 12),
                        ),
                      ),
                      onTap: () {
                        lobbyIdController.text = lobby.lobbyId;
                      },
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: Container(
        padding: EdgeInsets.all(10),
        color: Color(0xFF0F3460),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Made by ',
              style: TextStyle(color: Colors.white70),
            ),
            GestureDetector(
              onTap: () {},
              child: Text(
                'emodi',
                style: TextStyle(color: Color(0xFF4FC3F7), fontWeight: FontWeight.bold),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
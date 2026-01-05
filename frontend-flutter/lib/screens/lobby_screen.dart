import 'package:flutter/material.dart';
import '../core/joinly_client.dart';
import '../core/models.dart';
import '../widgets/player_tile.dart';
import '../widgets/ready_button.dart';

class LobbyScreen extends StatefulWidget {
  final JoinlyClient client;
  final String lobbyId;
  final String playerId;
  
  const LobbyScreen({
    Key? key,
    required this.client,
    required this.lobbyId,
    required this.playerId,
  }) : super(key: key);
  
  @override
  _LobbyScreenState createState() => _LobbyScreenState();
}

class _LobbyScreenState extends State<LobbyScreen> {
  Lobby? lobby;
  bool isReady = false;
  bool loading = true;
  
  @override
  void initState() {
    super.initState();
    loadLobby();
    startPolling();
  }
  
  void startPolling() {
    Future.delayed(Duration(seconds: 2), () {
      if (mounted) {
        loadLobby();
        startPolling();
      }
    });
  }
  
  Future<void> loadLobby() async {
    try {
      final data = await widget.client.getLobby(widget.lobbyId);
      setState(() {
        lobby = data;
        loading = false;
      });
    } catch (e) {
      print('Error loading lobby: $e');
    }
  }
  
  Future<void> toggleReady() async {
    setState(() {
      isReady = !isReady;
    });
    
    try {
      await widget.client.setReady(widget.lobbyId, widget.playerId, isReady);
      await loadLobby();
    } catch (e) {
      print('Error setting ready: $e');
    }
  }
  
  Future<void> leaveLobby() async {
    try {
      await widget.client.leaveLobby(widget.lobbyId, widget.playerId);
      Navigator.pop(context);
    } catch (e) {
      print('Error leaving lobby: $e');
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFF1A1A2E),
      appBar: AppBar(
        title: Text('Lobby: ${widget.lobbyId}'),
        backgroundColor: Color(0xFF0F3460),
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: loadLobby,
          ),
        ],
      ),
      body: loading
          ? Center(child: CircularProgressIndicator(color: Color(0xFF4FC3F7)))
          : lobby == null
              ? Center(child: Text('Lobby not found'))
              : Column(
                  children: [
                    Container(
                      padding: EdgeInsets.all(20),
                      color: Color(0xFF16213E),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceAround,
                        children: [
                          Text(
                            'Players: ${lobby!.playerCount}/${lobby!.maxPlayers}',
                            style: TextStyle(color: Colors.white, fontSize: 16),
                          ),
                          Text(
                            'Bots: ${lobby!.botCount}/${lobby!.maxBots}',
                            style: TextStyle(color: Colors.white, fontSize: 16),
                          ),
                          Container(
                            padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                            decoration: BoxDecoration(
                              color: lobby!.state == 'ready' ? Color(0xFF27AE60) : Color(0xFFF39C12),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Text(
                              lobby!.state.toUpperCase(),
                              style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                            ),
                          ),
                        ],
                      ),
                    ),
                    Expanded(
                      child: GridView.builder(
                        padding: EdgeInsets.all(20),
                        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                          crossAxisCount: 2,
                          childAspectRatio: 1.5,
                          crossAxisSpacing: 15,
                          mainAxisSpacing: 15,
                        ),
                        itemCount: lobby!.players.length + lobby!.bots.length,
                        itemBuilder: (context, index) {
                          if (index < lobby!.players.length) {
                            return PlayerTile(player: lobby!.players[index]);
                          } else {
                            final botIndex = index - lobby!.players.length;
                            return PlayerTile(bot: lobby!.bots[botIndex]);
                          }
                        },
                      ),
                    ),
                    Container(
                      padding: EdgeInsets.all(20),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          ReadyButton(
                            isReady: isReady,
                            onPressed: toggleReady,
                          ),
                          SizedBox(width: 20),
                          ElevatedButton(
                            onPressed: leaveLobby,
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Color(0xFF546E7A),
                              padding: EdgeInsets.symmetric(horizontal: 40, vertical: 15),
                            ),
                            child: Text('Leave Lobby'),
                          ),
                        ],
                      ),
                    ),
                  ],
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
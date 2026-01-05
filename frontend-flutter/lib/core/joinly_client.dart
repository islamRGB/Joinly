import 'dart:convert';
import 'package:http/http.dart' as http;
import 'models.dart';

class JoinlyClient {
  final String baseUrl;
  
  JoinlyClient({required this.baseUrl});
  
  Future<List<Lobby>> getLobbies() async {
    final response = await http.get(Uri.parse('$baseUrl/api/lobbies'));
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return (data['lobbies'] as List).map((l) => Lobby.fromJson(l)).toList();
    }
    throw Exception('Failed to load lobbies');
  }
  
  Future<Lobby> getLobby(String lobbyId) async {
    final response = await http.get(Uri.parse('$baseUrl/api/lobbies/$lobbyId'));
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return Lobby.fromJson(data['lobby']);
    }
    throw Exception('Failed to load lobby');
  }
  
  Future<Lobby> createLobby(String lobbyId, Map<String, dynamic> config) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/lobbies'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'lobby_id': lobbyId, 'config': config}),
    );
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return Lobby.fromJson(data['lobby']);
    }
    throw Exception('Failed to create lobby');
  }
  
  Future<Player> joinLobby(String lobbyId, String playerId, String username) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/lobbies/$lobbyId/join'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'player_id': playerId,
        'username': username,
        'metadata': {}
      }),
    );
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return Player.fromJson(data['player']);
    }
    throw Exception('Failed to join lobby');
  }
  
  Future<void> leaveLobby(String lobbyId, String playerId) async {
    await http.post(
      Uri.parse('$baseUrl/api/lobbies/$lobbyId/leave'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'player_id': playerId}),
    );
  }
  
  Future<void> setReady(String lobbyId, String playerId, bool ready) async {
    await http.post(
      Uri.parse('$baseUrl/api/lobbies/$lobbyId/ready'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'player_id': playerId, 'ready': ready}),
    );
  }
  
  Future<void> addBot(String lobbyId, String profile) async {
    await http.post(
      Uri.parse('$baseUrl/api/lobbies/$lobbyId/bots'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'profile': profile}),
    );
  }
}
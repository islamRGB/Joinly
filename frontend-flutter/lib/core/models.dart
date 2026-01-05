class Lobby {
  final String lobbyId;
  final String state;
  final int playerCount;
  final int botCount;
  final int maxPlayers;
  final int maxBots;
  final List<Player> players;
  final List<Bot> bots;
  
  Lobby({
    required this.lobbyId,
    required this.state,
    required this.playerCount,
    required this.botCount,
    required this.maxPlayers,
    required this.maxBots,
    required this.players,
    required this.bots,
  });
  
  factory Lobby.fromJson(Map<String, dynamic> json) {
    return Lobby(
      lobbyId: json['lobby_id'],
      state: json['state'],
      playerCount: json['player_count'],
      botCount: json['bot_count'],
      maxPlayers: json['max_players'],
      maxBots: json['max_bots'],
      players: (json['players'] as List).map((p) => Player.fromJson(p)).toList(),
      bots: (json['bots'] as List).map((b) => Bot.fromJson(b)).toList(),
    );
  }
}

class Player {
  final String playerId;
  final String username;
  final bool ready;
  final int? team;
  final bool connected;
  
  Player({
    required this.playerId,
    required this.username,
    required this.ready,
    this.team,
    required this.connected,
  });
  
  factory Player.fromJson(Map<String, dynamic> json) {
    return Player(
      playerId: json['player_id'],
      username: json['username'],
      ready: json['ready'],
      team: json['team'],
      connected: json['connected'],
    );
  }
}

class Bot {
  final String botId;
  final String username;
  final bool ready;
  final int? team;
  final String behavior;
  
  Bot({
    required this.botId,
    required this.username,
    required this.ready,
    this.team,
    required this.behavior,
  });
  
  factory Bot.fromJson(Map<String, dynamic> json) {
    return Bot(
      botId: json['bot_id'],
      username: json['username'],
      ready: json['ready'],
      team: json['team'],
      behavior: json['behavior'],
    );
  }
}
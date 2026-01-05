import 'package:flutter/material.dart';
import '../core/models.dart';

class PlayerTile extends StatelessWidget {
  final Player? player;
  final Bot? bot;
  
  const PlayerTile({Key? key, this.player, this.bot}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    final isPlayer = player != null;
    final username = isPlayer ? player!.username : bot!.username;
    final ready = isPlayer ? player!.ready : bot!.ready;
    
    return Container(
      decoration: BoxDecoration(
        color: Color(0xFF16213E),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: ready ? Color(0xFF27AE60) : Color(0xFF1E5F8C),
          width: 2,
        ),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            isPlayer ? Icons.person : Icons.smart_toy,
            size: 40,
            color: Color(0xFF4FC3F7),
          ),
          SizedBox(height: 10),
          Text(
            username,
            style: TextStyle(
              color: Colors.white,
              fontSize: 16,
              fontWeight: FontWeight.bold,
            ),
            textAlign: TextAlign.center,
          ),
          SizedBox(height: 5),
          Container(
            padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
            decoration: BoxDecoration(
              color: isPlayer ? Color(0xFF3498DB) : Color(0xFFF39C12),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Text(
              isPlayer ? 'PLAYER' : 'BOT',
              style: TextStyle(
                color: Colors.white,
                fontSize: 12,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          if (ready)
            Padding(
              padding: EdgeInsets.only(top: 8),
              child: Icon(
                Icons.check_circle,
                color: Color(0xFF27AE60),
                size: 24,
              ),
            ),
        ],
      ),
    );
  }
}
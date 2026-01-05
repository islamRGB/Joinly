import 'package:flutter/material.dart';

class ReadyButton extends StatelessWidget {
  final bool isReady;
  final VoidCallback onPressed;
  
  const ReadyButton({
    Key? key,
    required this.isReady,
    required this.onPressed,
  }) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: isReady ? Color(0xFFE74C3C) : Color(0xFF27AE60),
        padding: EdgeInsets.symmetric(horizontal: 40, vertical: 15),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            isReady ? Icons.close : Icons.check,
            color: Colors.white,
          ),
          SizedBox(width: 10),
          Text(
            isReady ? 'Not Ready' : 'Ready Up',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
        ],
      ),
    );
  }
}
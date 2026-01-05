# Joinly Control Panel

Web-based admin dashboard for managing the Joinly multiplayer lobby system.

## Features

- **Real-time Monitoring**: Live updates of lobbies, players, and bots
- **Lobby Management**: Create and delete lobbies
- **Player Tracking**: Monitor connected players
- **Bot Control**: Create and manage AI players
- **Matchmaking**: View queue statistics
- **Event Logs**: Real-time event monitoring
- **Responsive Design**: Works on desktop, tablet, and mobile

## Quick Start

### Running the Control Panel

The control panel is automatically served by the Joinly backend:

```bash
cd backend
python launcher.py
```

This will:
1. Start the backend server
2. Open the control panel in your browser
3. Navigate to `http://localhost:5000/control`

### Manual Access

You can also access the control panel directly:

```
http://localhost:5000/control
```

## Panels

### Lobbies
- View all active lobbies
- Create new lobbies with custom configuration
- Delete lobbies
- Monitor lobby states and player counts

### Players
- See all connected players
- View player statistics
- Monitor connection status
- Track skill ratings

### Bots
- Create bots with different profiles
- Manage active bots
- View bot behaviors
- Remove bots from system

### Matchmaking
- View matchmaking queues
- Create custom queues
- Monitor queue lengths
- Track average wait times

### Logs
- Real-time event monitoring
- View system events
- Filter by event type
- Clear event history

## UI Components

### Navigation
- Sidebar with panel selection
- Active panel highlighting
- Smooth transitions

### Cards
- Lobby cards with state badges
- Player cards with status
- Bot cards with behavior tags
- Queue cards with statistics

### Actions
- Primary buttons for creation
- Secondary buttons for views
- Danger buttons for deletion
- Status badges for states

## Customization

### Colors

The control panel uses a blue tech theme:
- Primary: `#4FC3F7` (Cyan Blue)
- Background: `#1A1A2E` (Dark)
- Cards: `#16213E` (Navy)
- Accent: `#0F3460` (Deep Blue)

### Styling

Edit `dashboard.css` to customize:
- Colors and gradients
- Card layouts
- Button styles
- Hover effects

### Branding

Update footer in `index.html`:
```html
<div class="footer">
    <p>Made by <a href="https://emodi.me">emodi</a> | Your Brand</p>
</div>
```

## API Integration

The control panel communicates with these endpoints:

- `GET /api/lobbies` - Fetch lobbies
- `POST /api/lobbies` - Create lobby
- `DELETE /api/lobbies/{id}` - Delete lobby
- `GET /api/players` - Fetch players
- `GET /api/bots` - Fetch bots
- `POST /api/bots` - Create bot
- `DELETE /api/bots/{id}` - Remove bot
- `GET /api/queues` - Fetch queues
- `GET /api/admin/events` - Fetch event logs

## WebSocket Events

Real-time updates via Socket.IO:
- `lobby_state` - Lobby updates
- `player_joined` - Player joins
- `player_left` - Player leaves
- `bot_added` - Bot additions

## Development

### File Structure

```
control-ui/
├── index.html        # Main HTML
├── dashboard.css     # Styles
├── assets/           # Images and resources
│   └── joinly_logo.png
└── README.md
```

### Testing Locally

1. Start backend: `python app.py`
2. Open browser: `http://localhost:5000/control`
3. Use browser dev tools for debugging

### Building for Production

No build step required - static HTML/CSS/JS.

Deploy files to any web server or CDN.

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance

- Auto-refresh every 5 seconds
- Efficient DOM updates
- Minimal JavaScript
- Fast page load (<1s)

## Troubleshooting

**Problem**: Control panel doesn't load
- Check backend is running
- Verify port 5000 is available
- Check browser console for errors

**Problem**: Data not updating
- Check WebSocket connection
- Verify CORS settings
- Refresh page manually

**Problem**: Styling issues
- Clear browser cache
- Check CSS file is loading
- Verify paths are correct

## Credits

Made by [emodi](https://emodi.me)

Part of the Joinly multiplayer lobby framework.
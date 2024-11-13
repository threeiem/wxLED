# wxLED - Weather LED Controller

Display current weather conditions using an RGB LED on a Raspberry Pi Zero W.

## Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install requirements:
```bash
pip install -e .
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run the application:
```bash
python -m weather_led
```

## Hardware Setup

Connect RGB LED to Raspberry Pi:
- Red → GPIO17
- Green → GPIO27
- Blue → GPIO22
- Ground → GND

## License

MIT

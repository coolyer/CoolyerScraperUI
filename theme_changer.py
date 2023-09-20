import json

def read_theme_settings(config_file):
    try:
        # Read the JSON config file
        with open("config.json", 'r') as f:
            config_data = json.load(f)

        # Get the theme settings from the config
        theme_settings = config_data.get("theme", {})
        theme_mode = theme_settings.get("enabled", True)
        background_color = theme_settings.get("background_color", "#181a1b")
        text_color = theme_settings.get("text_color", "#ffffff")
        buttons_color = theme_settings.get("buttons_color", "#ffffff")
        text_size = theme_settings.get("text_size", "12pt")
        font_style = theme_settings.get("font_style", "Arial")
        print("Theme enabled")
        if not theme_mode:
            # theme_mode is False, use default colors
            print("Theme not enabled, using default colors")
            return False, "#181a1b", "#ffffff", "#00aaff", "12pt", "Arial"
        
        return theme_mode, background_color, text_color, buttons_color, text_size, font_style
    except Exception as e:
        print(f"Error reading theme settings: {str(e)}")
        return False, "#181a1b", "#ffffff", "#00aaff", "12pt", "Arial"
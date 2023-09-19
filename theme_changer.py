import json

def read_theme_settings(config_file):
    try:
        # Read the JSON config file
        with open("config.json", 'r') as f:
            config_data = json.load(f)

        # Get the theme settings from the config
        theme_settings = config_data.get("theme", {})
        theme_mode = theme_settings.get("enabled", True)
        background_color = theme_settings.get("background_color", "#ffffff")
        text_color = theme_settings.get("text_color", "#000000")
        buttons_color = theme_settings.get("buttons_color", "#ffffff")
        

        if not theme_mode:
            # theme_mode is False, use default colors
            return False, "#ffffff", "#000000", "#ffffff"
        
        return theme_mode, background_color, text_color, buttons_color
    except Exception as e:
        print(f"Error reading theme settings: {str(e)}")
        return False, "#ffffff", "#000000", "#ffffff"
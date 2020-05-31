import sublime_plugin, subprocess, sublime

class FontFaceSwitcherCommand(sublime_plugin.TextCommand):
    def input(self, args):
        return FontFaceSwitcherMain()


class FontFaceSwitcherMain(sublime_plugin.ListInputHandler):
    pref = None
    fonts = None
    old_font_face = None
    new_font_face = None

    def __init__(self):
        self.pref = sublime.load_settings('Preferences.sublime-settings')

        self.old_font_face = self.pref.get('font_face')

    def name(self):
        return 'FontFaceSwitcherMain'

    def initial_text(self):
        return self.old_font_face

    def preview(self, value):
        if value is not '':
            # No way to know if set passed/failed
            # http://www.sublimetext.com/docs/3/api_reference.html#sublime.Settings
            self.pref.set('font_face', value)
            self.new_font_face = value

        return None

    # revert old font_face on cancel
    def cancel(self):
        self.pref.set('font_face', self.old_font_face)
        return None

    def confirm(self, value):
        self.pref.set('font_face', self.new_font_face)
        sublime.save_settings('Preferences.sublime-settings')
        return None

    def list_items(self):
        if self.fonts is None:
            try:
                output = subprocess.check_output('fc-list --format="%{fullname}\n"', shell=True)
                output = set(output.strip().decode().split('\n'))
                self.fonts = list(output)
            except:
                self.fonts = ['']

        return self.fonts


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import time
from datetime import datetime
from playsound import playsound
import threading
from kivy.properties import ObjectProperty
from kivy.uix.checkbox import CheckBox
import os
'''Metronome beast version 0.0.1'''

class MainWidget(BoxLayout):
    #hello_label = ObjectProperty()
    #name_input = ObjectProperty()
    bpm_input = ObjectProperty()
    beats_input = ObjectProperty()
    accent_enabled = ObjectProperty()
    #accent_enabled = ids.checkbox
    prjct_path = os.path.dirname(os.path.abspath(__file__))
    click_accented = f"{prjct_path}/source/audio/click_accented_long.wav"
    click_normal = f"{prjct_path}/source/audio/click_normal.wav"
    
    def say_hello(self):
        print('тест кнопки')
        #self.hello_label.text = 'Привет ' + self.name_input.text

        # get beats per minute value
    def get_bpm(self, *args):
        try:
            bpm_value = int(self.bpm_input.text)
            return bpm_value
        except ValueError:
            print("Invalid bpm entry")
            return 0

    def get_tpb(self, *args):
        # print('ticks per beat arguments: ' + str(args))
        try:
            tpb_value = int(self.beats_input.text)
            print('ticks per bar: {}'.format(tpb_value))
            return tpb_value
        except ValueError:
            print("Invalid tpb entry")
            return 0
    
    def more_than_2_threads(self):
        print(threading.enumerate())
        return len(threading.enumerate()) > 2


    def tick(self, tick_enabled):
        #time.sleep(1)
        bpm_value = self.get_bpm()
        print('bpm value: ' + str(bpm_value))
        tpb_value = self.get_tpb()
        print('53'+ ' ' + str(threading.get_ident()))
        # print('{}, {}'.format(bpm_value, tick_enabled))
        ####ВОТ ТУТ КАКА
        #print('accented click enabled: {}'.format(self.accent_enabled.active))
        t0 = datetime.now()
        print(t0)
        num_of_ticks = 0
        print(59)
        if bpm_value == 0 or tpb_value == 0:
            return
        time_per_beat = 60 / bpm_value  # time in [s]
        print(63)
        while tick_enabled:
            # print(bpm_value)
            print(threading.get_ident())
            print(threading.enumerate()[1].ident)
            if self.more_than_2_threads() and threading.get_ident() == threading.enumerate()[1].ident:
                print(f'more than 2 {self.more_than_2_threads()}')
                break
            if tpb_value == 0:
                break

            #if self.accent_enabled.active:
            if True:
                start = time.time()
                playsound(self.click_accented)
                #play_click_accented = click_accented.play()  # plays 0.05s
                #play_click_accented.wait_done()
                num_of_ticks += 1
                print(f'num_of_ticks = {num_of_ticks}')
                if self.more_than_2_threads() and threading.get_ident() == threading.enumerate()[1].ident:
                    break
                end = time.time()
                delay = end - start
                # print(delay)
                if delay < time_per_beat:
                    time.sleep(time_per_beat - delay)  # click_accented_long.waw is 0.03s longer
            else:
                start = time.time()
                playsound(self.click_normal)
                #play_click_normal = click_normal.play()  # plays 0.02s
                #play_click_normal.wait_done()
                num_of_ticks += 1
                end = time.time()
                delay = end - start
                # print(delay)
                if self.more_than_2_threads() and threading.get_ident() == threading.enumerate()[1].ident:
                    break
                time.sleep(time_per_beat - delay)

            for i in range(tpb_value - 1):
                start = time.time()
              #  print(f'start = {start}')
                if self.more_than_2_threads() and threading.get_ident() == threading.enumerate()[1].ident:
                    break
                playsound(self.click_normal)
                ##play_click_normal = click_normal.play()  # plays 0.02s
                #play_click_normal.wait_done()
                num_of_ticks += 1
                end = time.time()
               # print(f'end = {end}')
                delay = end - start
                time.sleep(time_per_beat - delay)
        
        if tick_enabled:
            t1 = datetime.now()
            t_delta = t1 - t0
            print("\n\n")
            print("Number of ticks: " + str(num_of_ticks))
            print("Time passed: " + str(t_delta))
            print("\n\n")
        else:
            threading.enumerate()[1].join()
        print('line 122')
        print(f'{print(threading.get_ident())} im killed?')

        
    def tick_threaded(self, enabled):
        if self.get_bpm() < 15:
            self.text_bpm.set(15)
        if self.get_bpm() > 450:
            self.text_bpm.set(450)

        num_of_ticks = 0
        thread = threading.Thread(target=self.tick, args=(enabled,))
        thread.start()
        num_of_ticks += 1
        if self.more_than_2_threads():
            # print(threading.get_ident())
            threading.enumerate()[1].join()
            print(threading.enumerate()[1])
            print('line 140')
            
            print('line 142')
        print(threading.enumerate())

    def exit_tick_threaded(self):
        if len(threading.enumerate()) > 1:
            print(threading.get_ident())
            threading.enumerate()[1].join()

class MainApp(App):

    def build(self):
        return MainWidget()


if __name__ == '__main__':
    app = MainApp()
    app.run()
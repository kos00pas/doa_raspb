import ReSpeaker_Mic4 as resp
import The_Data_Class
from The_Main_Window import Main_Window


class GUIManager:
    def __init__(self,resp4_resp):
        print("here")
        self.DATA = The_Data_Class.Data_Class(resp4=resp4_resp ) #1
        self.main_window = Main_Window( self,self.DATA ) #2
        self.DATA.main_window=self.main_window #3
        self.main_window.mainloop( ) #4

if __name__ == '__main__':
    resp4=resp.ReSpeaker_Mic4( ) #1
    print("respeaker_set")
    GUIManager( resp4_resp=resp4 ) #

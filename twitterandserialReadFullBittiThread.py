# -- coding: utf-8
#eyer ekrana uyari yazisi gostermek istiyorsan 
# self.showMessage(title,message ,number)
# number == 1 warning
# number == 2 info  olarak ayarlandi


#twitter importlari
from Tkinter import *
from twython import Twython, TwythonError
import sys
import tkFont
import tkMessageBox
#mysql importlari
from mysql.connector import MySQLConnection, Error
from m3dbConfig import read_db_config
import sys, tty, termios
import serial
#thread import ettik
from threading import Thread

class TwitterGUI(Frame):
    def __init__(self, master):
	Frame.__init__(self, master)
        self.master = master
        master.title("Turab Otomation")

	#Burada ekran boyutlarini aldik 
	sw=master.winfo_screenwidth()
        sh=master.winfo_screenheight()
	#tam ekran yapma ayari
	master.attributes('-fullscreen', True)
	#yukaridan aldigimiz ekran boyutlarini uygulama boyutlari olarak atadik
	master.geometry('%dx%d' % ( sw,sh) )
	#olusturdugumuz arayuzun arka plan rengini siyah yaptik
	master.configure(background="black")
	#Burada arayuzu bolumlere ayirdik 	
	topframe=Frame(master)
        topframe.pack(side=TOP,pady=40)

        middleframe = Frame(master)
        middleframe.pack( side = TOP,pady=30)

        bottomframe = Frame(master)
        bottomframe.pack( side = TOP)

        bottomframeEnter = Frame(master,bg="black")
        bottomframeEnter.pack(side=TOP, anchor=W,fill=BOTH,  expand=YES)

	#olusturacagimiz textlere buradan font olusturduk kullacagimiz yerde sadece bu isimleri
	#tanimlamamiz yeterli olacaktir
        customFont = tkFont.Font(family="{MS Sans Serif} bold", size=60)
        customFont2 = tkFont.Font(family="Helvetica bold", size=20)
        customFont3 = tkFont.Font(family="Helvetica bold", size=12)


	T1= Label(topframe,text="TWITTER", font=customFont,fg="white",bg="black")
        T2= Label(middleframe,text="Elektronik Takip  Sistemi Uzerine Kurulu \nSosyal Sorumluluk Projesi ", font=customFont2,fg="white",bg="black")
        T3= Label(bottomframe,text="Bu cihazi kullandiginizi Twitter'da paylasmak ister misiniz?", font=customFont3,fg="white",bg="black")
        T1.pack()
        T2.pack()
        T3.pack(padx=10)
        L1 = Label(bottomframeEnter,width=20, text="Twitter Adinizi Giriniz: ",fg="white",bg="black")
        L1.pack(side=LEFT, anchor=W,expand=NO)
        self. E1 = Entry(bottomframeEnter)
        self.E1.pack(side=LEFT, anchor=W,fill=X, expand=YES,padx=20)
	#uygulama ilk acilista entery'i aktif hale getiriyoruz
	self.E1.focus_set()
	#klavye  kisayollari tanimladim
	master.bind("<Control-c>",self.quit)
	#Burada enter tusuna basmayi Return ile yapiyoruz
        self.E1.bind("<Return>",self.twitter)
	#cok onemli thread lerimiz burada tanimladik ve start ettik
	try:
		threadSerial = Thread(target = self.serialRead)
        	threadTwit = Thread(target = self.twitter)
		threadSerial.daemon = True
		threadTwit.daemon = True
	        threadSerial.start()
        	threadTwit.start()
	except Error as e:
		print e
	# ekrana uyari yazilarini yazdirmak icin tanimladigimiz bolum
    def showMessage(self,title,message,number):
	if number==1:
	        tkMessageBox.showwarning(title,message)
	elif number==2:
		tkMessageBox.showinfo(title,message)
	#twit atildiktan sonra veya enter 'e basildiktan sonra entery'nin icini siler
    def clear_text(self):
	self.E1.delete(0, END)
	self.E1.insert(0, "")
    
	#twitter apilerini tanimladigimiz ve twittter attimiz bolum
	#self yazmamizin sebebi istedigim her yerden ulasmam yani global olarak tanimladim
	#event yazmamin sebebi ise klavye kisayollarini kullanama bilmem
    def twitter(self,event=NONE):
       try:
	tweetStr = ("HURDACI SOSYAL SORUMLULUK PROJESINI KULLANDIGIN ICIN TESEKKUR EDERIZ"+'%s' % (self.E1.get()))
        apiKey = '*******************'
        apiSecret = '***************************'
        accessToken = '**********************************'
        accessTokenSecret = '******************************'
        api = Twython(apiKey,apiSecret,accessToken,accessTokenSecret)
        if len(tweetStr)<= 140:
                api.update_status(status=tweetStr)
                print "twit atildi"
                tweetStr = tweetStr + "s"
                print "len: ",len(tweetStr)
		self.showMessage("Tesekkurler", "Twit Basari Ile Atildi",2)
		self.clear_text()
        else:
                print "140 karakter sorunu"
                self.showMessage("hata", "Twitter 140 Karakter Sinirini Astiniz",1)
		self.clear_text()
	return "1"
       except TwythonError as e:
	print "Error Gelmedimi: ", e
	self.showMessage("hata", "Ayni twiti bir kere atabilirsiniz.",1)
	self.clear_text()
        return "0"
	# klavye kisayollarini kullanarak cikmam icin
    def quit(self,event):
        print("quitting...")
        sys.exit(0)
        self.destroy()
#class  mysImportTime(object):
#    def __init__(self, master):
#	self.serialRead()
    def insert_pil(self,adetPi):
		query = "INSERT INTO hurda_pil(adet) " \
            	"VALUES(%s)"
		args = (adetPi)

		try:
	         db_config = read_db_config()
	         conn = MySQLConnection(**db_config)

	         cursor = conn.cursor()
	         cursor.execute(query, args)

        	 if cursor.lastrowid:
	            print('last insert id', cursor.lastrowid)
        	 else:
	            print('last insert id not found')

        	 conn.commit()
		except Error as error:
		        print(error)

		finally:
		 cursor.close()
		 conn.close()

    def insert_plastik(self,adetPlastk):
		query = "INSERT INTO hurda_plastik(adet) " \
	        	"VALUES(%s)"
		args = (adetPlastk)

		try:
	         db_config = read_db_config()
	         conn = MySQLConnection(**db_config)

	         cursor = conn.cursor()
	         cursor.execute(query, args)

	         if cursor.lastrowid:
        	  print('last insert id', cursor.lastrowid)
	         else:
        	  print('last insert id not found')

	         conn.commit()
		except Error as error:
	         print(error)

		finally:
	         cursor.close()
	         conn.close()
    def insert_teneke(self,adetTeneke):
	 query = "INSERT INTO hurda_teneke(adet) " \
            "VALUES(%s)"
   	 args = (adetTeneke)

   	 try:
        	db_config = read_db_config()
	        conn = MySQLConnection(**db_config)

        	cursor = conn.cursor()
	        cursor.execute(query, args)

        	if cursor.lastrowid:
	            print('last insert id', cursor.lastrowid)
        	else:
	            print('last insert id not found')

        	conn.commit()
	 except Error as error:
	        print(error)

	 finally:
	        cursor.close()
        	conn.close()
    def serialRead(self):
	while (1):
	        seri = serial.Serial('/dev/ttyACM0', 9600)
#       seri.open()
        	try:
                	data=seri.read()
	                print data
        	        if data == '1':
        	                self.insert_pil('1'),
                	elif data == '2':
                	        self.insert_teneke('1'),
	                elif data == '3':
        	                self.insert_plastik('1')
	                else:
        	                print 'serial yanlis deger geldi'

	        except RuntimeError:
        	        print 'def serial runtime error'
	        except KeyboardInterrupt:
        	        print 'def serial klavye hatasi'
               		sys.exit(0)
#               seri.close()
#Referanslari tanimladim ve atadim
if __name__ == '__main__':
	root = Tk()
	my_gui = TwitterGUI(root)
#islemin surekli tekrar etmesi icin
	root.mainloop()

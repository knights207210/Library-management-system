# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
import Pmw
import sqlite3
import time

#database connection
conn=sqlite3.connect("library.db")
c=conn.cursor() 

#main interface
class Application(Frame):
	def __init__(self,master=None):
		Frame.__init__(self, master)
		self.pack()
		self.set_window()
		Pmw.initialise(root)		    #初始化
	def set_window(self):
		global enter_ID
		global Ad_rbs
		global Stu_rbs
		Stu_rbs=0
		Ad_rbs=0
		self.im = PhotoImage(file="3.png")
		root.resizable(False, False)
		window=Label(root,image=self.im,text='top.resizable(False, False)')
		w = self.im.width()
		root.geometry("%dx%d+0+0" % (w, 300))
		window.pack()
		root.configure(background='#b0c4de')
		ID = Label(root,text='ID',font='YaHei 16 bold',compound='center').place(x=30,y=80)
		enter_ID = Entry(root)
		enter_ID.place(x=120,y=85,width='180')
		GO= ttk.Button(root,text='GO',command=self.GO_click).place(x=330,y=82,width='40')
		v = IntVar()
		Stu_rb = Radiobutton(root,text='Student',command=self.Stu_rb_click,font='YaHei 12 bold',value=1,variable=v).place(x=80,y=180)
		Ad_rb = Radiobutton(root,text='Administrator',command=self.Ad_rb_click,font='YaHei 12 bold',value=2,variable=v).place(x=210,y=180)             #设置主窗口
	def Stu_rb_click(self):           #选中学生
		global Stu_rbs
		global Ad_rbs
		Ad_rbs=0
		Stu_rbs=1
		
	def Ad_rb_click(self):
		global Ad_rbs
		global Stu_rbs
		Stu_rbs=0
		Ad_rbs=2
		            #select ad          #选中管理员
	
	def GO_click(self):               #单击Go出现下一级界面
		key1=False
		key2=False
		global IDstring

		#global Stu_rbs
		#global Ad_rbs
		def Stu_borro2_click():
			global countable
			global count
			global row
			global IDstring
			global e5
			global f5
			global Stu_borro1_dropdown
			timetrans='%Y-%m-%d %X'
			timestring=time.strftime(timetrans,time.localtime())
			if countable==0:
				borout=Toplevel()
				Label(borout,text='此书已借完').pack()
				ttk.Button(borout,text='确定',command=borout.withdraw).pack()
				return
			countable-=1
			count+=1
			c.execute("UPDATE booklist SET leftnum=leftnum-1 WHERE ISBN=?",(row[0],))
			c.execute("UPDATE booklist SET borrowed=borrowed+1 WHERE ISBN=?",(row[0],))
			c.execute("INSERT INTO borrow VALUES(?,?,?,'-')",(row[0],IDstring,timestring))
			conn.commit()
			success1=Toplevel()
			Label(success1,text='借书成功！').pack()
			ttk.Button(success1,text='确定',command=success1.withdraw).pack()
			if Stu_borro1_dropdown.get()=='索书号':
				e5.set(str(countable))
			if Stu_borro1_dropdown.get()=='ISBN':
				f5.set(str(countable))     #单击借阅执行

		def Stu_back_click(): 
			global countable         #可借量         
			global count             #剩余量
			global row               #select 选中的元组  两个if二选一得到
			global IDstring          #第一级界面的entry内容
			global e5                #索书号剩余量set
			global f5                #ISBN剩余量
			global Stu_borro1_dropdown    #第二级学生借还书界面下拉菜单 
			timetrans='%Y-%m-%d %X'
			timestring=time.strftime(timetrans,time.localtime())
			countable+=1
			count-=1
			if(count<0):
				x=Toplevel()
				x_label=Label(x,text='操作异常').pack()
				x_b=ttk.Button(x,text='确定',command=x.withdraw).pack()
				return
			else:
				c.execute("UPDATE booklist SET leftnum=leftnum+1 WHERE ISBN=?",(row[0],))
				c.execute("UPDATE booklist SET borrowed=borrowed-1 WHERE ISBN=?",(row[0],))
				c.execute("INSERT INTO borrow VALUES(?,?,'-',?)",(row[0],IDstring,timestring))
				conn.commit()
				success2=Toplevel()
				Label(success2,text='还书成功！').pack()
				ttk.Button(success2,text='确定',command=success2.withdraw).pack()
				if Stu_borro1_dropdown.get()=='索书号':
					e5.set(str(countable))
				if Stu_borro1_dropdown.get()=='ISBN':
					f5.set(str(countable))      #单击退还执行

		def Stu_borro1_click():      #学生借还界面确定按钮触发
			key3=False
			key4=False
			global e5
			global f5
			global countable
			global count
			global Stu_borro1_dropdown
			global IDstring
			global row
			if Stu_borro1.get()=='':
				error=Toplevel()
				Label(error,text='内容不能为空').pack()
				ttk.Button(error,text='确定',command=error.withdraw).pack()
				return
			if Stu_borro1.get()!='':
				if Stu_borro1_dropdown.get()=='索书号':
					for k in c.execute('SELECT num FROM booklist'):
						pass
						for y in k:
							if y==Stu_borro1.get():
								key3=True
					if (key3==False):
						exe10=Toplevel()
						Label(exe10,text='该书不存在，请重新输入').pack()
						ttk.Button(exe10,text='确定',command=exe10.withdraw).pack()
						return
					if(key3==True):
						s='%'+Stu_borro1.get()+'%' 
						for x in c.execute("SELECT * FROM booklist WHERE num LIKE ?",(s,)):
							row=x
							e11=x[1]
							e22=x[3]
							e33=x[5]
							e44=x[4]
							e55=x[8]
							countable=x[8]
							count=x[9]


					name1=Label(Stu_f2,text='书名',font='YaHei 12 bold',compound='center').place(x=20,y=150)
					e1=StringVar()
					Stu_borro2=Entry(Stu_f2,textvariable = e1)
					e1.set(e11)
					Stu_borro2.place(x=80,y=150,width=600,height=26)
					Stu_borro2['state']='readonly'
					name2=Label(Stu_f2,text='作者',font='YaHei 12 bold',compound='center').place(x=20,y=200)
					e2=StringVar()
					Stu_borro3=Entry(Stu_f2,textvariable = e2)
					e2.set(e22)
					Stu_borro3.place(x=80,y=200,width=180,height=24)
					Stu_borro3['state']='readonly'

					name3=Label(Stu_f2,text='出版年份',font='YaHei 12 bold',compound='center').place(x=280,y=200)
					e3=StringVar()
					Stu_borro4=Entry(Stu_f2,textvariable = e3)
					e3.set(e33)
					Stu_borro4.place(x=375,y=200,width=300,height=24)
					Stu_borro4['state']='readonly'

					name4=Label(Stu_f2,text='出版社',font='YaHei 12 bold',compound='center').place(x=20,y=250)
					e4=StringVar()
					Stu_borro5=Entry(Stu_f2,textvariable = e4)
					e4.set(e44)
					Stu_borro5.place(x=100,y=250,width=300,height=24)
					Stu_borro5['state']='readonly'

					name5=Label(Stu_f2,text='可借量',font='YaHei 12 bold',compound='center').place(x=415,y=250)
					e5=StringVar()
					Stu_borro6=Entry(Stu_f2,textvariable = e5)
					e5.set(e55)
					Stu_borro6.place(x=490,y=250,width=190,height=24)
					Stu_borro6['state']='readonly'

					name6=Label(Stu_f2,text='读者ID',font='YaHei 12 bold',compound='center').place(x=150,y=375)
					e6=StringVar()
					Stu_borro7=Entry(Stu_f2,textvariable = e6)
					e6.set(IDstring)
					Stu_borro7.place(x=260,y=375,width=300,height=24)
					Stu_borro7['state']='readonly'

				if Stu_borro1_dropdown.get()=='ISBN':
					for k1 in c.execute('SELECT ISBN FROM booklist'):
						pass
						for y1 in k1:
							if y1==Stu_borro1.get():
								key4=True
					if (key4==False):
						exe11=Toplevel()
						Label(exe11,text='该书不存在，请重新输入').pack()
						ttk.Button(exe11,text='确定',command=exe11.withdraw).pack()
						return
					if(key4==True):
						s12='%'+Stu_borro1.get()+'%' 
						for x1 in c.execute("SELECT * FROM booklist WHERE ISBN LIKE ?",(s12,)):
							row=x1
							e111=x1[1]
							e222=x1[3]
							e333=x1[5]
							e444=x1[4]
							e555=x1[8]
							countable=x1[8]
							count=x1[9]
						name1=Label(Stu_f2,text='书名',font='YaHei 12 bold',compound='center').place(x=20,y=150)
						f1=StringVar()
						Stu_borro2=Entry(Stu_f2,textvariable = f1)
						f1.set(e111)
						Stu_borro2.place(x=80,y=150,width=600,height=26)
						Stu_borro2['state']='readonly'

						name2=Label(Stu_f2,text='作者',font='YaHei 12 bold',compound='center').place(x=20,y=200)
						f2=StringVar()
						Stu_borro3=Entry(Stu_f2,textvariable = f2)
						f2.set(e222)
						Stu_borro3.place(x=80,y=200,width=180,height=24)
						Stu_borro3['state']='readonly'

						name3=Label(Stu_f2,text='出版年份',font='YaHei 12 bold',compound='center').place(x=280,y=200)
						f3=StringVar()
						Stu_borro4=Entry(Stu_f2,textvariable = f3)
						f3.set(e333)
						Stu_borro4.place(x=375,y=200,width=300,height=24)
						Stu_borro4['state']='readonly'

						name4=Label(Stu_f2,text='出版社',font='YaHei 12 bold',compound='center').place(x=20,y=250)
						f4=StringVar()
						Stu_borro5=Entry(Stu_f2,textvariable = f4)
						f4.set(e444)
						Stu_borro5.place(x=100,y=250,width=300,height=24)
						Stu_borro5['state']='readonly'

						name5=Label(Stu_f2,text='可借量',font='YaHei 12 bold',compound='center').place(x=415,y=250)
						f5=StringVar()
						Stu_borro6=Entry(Stu_f2,textvariable = f5)
						f5.set(e555)
						Stu_borro6.place(x=490,y=250,width=190,height=24)
						Stu_borro6['state']='readonly'

						name6=Label(Stu_f2,text='读者ID',font='YaHei 12 bold',compound='center').place(x=150,y=375)
						e6=StringVar()
						Stu_borro7=Entry(Stu_f2,textvariable = e6)
						e6.set(IDstring)
						Stu_borro7.place(x=260,y=375,width=300,height=24)
						Stu_borro7['state']='readonly'


	


		def Stu_query_click():                          #书籍查询界面
			global Stu_dropdown
			global Stu_query
			Stu_query_table=Toplevel()                        
			Stu_query_table.title('书籍查询')
			table=ttk.Treeview(Stu_query_table,columns=('col1','col2','col3','col4','col5','col6','col7','col8','col9','col10'))   
			table.column('col1', width=100, anchor='w')  
			table.column('col2', width=180, anchor='w')
			table.column('col3', width=100, anchor='w')
			table.column('col4', width=100, anchor='w')
			table.column('col5', width=150, anchor='w')
			table.column('col6', width=70,  anchor='center')
			table.column('col7', width=120, anchor='w')
			table.column('col8', width=200, anchor='center')
			table.column('col9', width=50, anchor='center')
			table.column('col10', width=50, anchor='center')
			table.heading('col1', text='ISBN')
			table.heading('col2', text='书名')
			table.heading('col3', text='索书号')
			table.heading('col4', text='作者')
			table.heading('col5', text='出版社')
			table.heading('col6', text='出版年份')
			table.heading('col7', text='书籍状态')
			table.heading('col8', text='馆藏地')
			table.heading('col9', text='可借量')
			table.heading('col10', text='借出量')
			if Stu_query.get()=='':
				for z in c.execute("SELECT * FROM booklist"):
					table.insert('',0,values=(z))
			if Stu_query.get()!='':
				if Stu_dropdown.get()=='关键字':
					s1='%'+Stu_query.get()+'%'
					c.execute("SELECT * FROM booklist WHERE title LIKE ?",(s1,))
					x1=c.fetchall()
					if(x1==[]):
						table.pack()
						notex1=Toplevel()
						Label(notex1,text='此书不存在').pack()
						ttk.Button(notex1,text='返回',command=notex1.withdraw).pack()
						return
					for x1 in c.execute("SELECT * FROM booklist WHERE title LIKE ?",(s1,)):
						table.insert('',0,values=(x1))
				elif Stu_dropdown.get()=='作者': 
					s2='%'+Stu_query.get()+'%'
					c.execute("SELECT * FROM booklist WHERE author LIKE ?",(s2,))
					x2=c.fetchall()
					if(x2==[]):
						table.pack()
						notex2=Toplevel()
						Label(notex2,text='此书不存在').pack()
						ttk.Button(notex2,text='返回',command=notex2.withdraw).pack()
						return
					for x2 in c.execute("SELECT * FROM booklist WHERE author LIKE ?",(s2,)):
						table.insert('',0,values=(x2))
				elif Stu_dropdown.get()=='出版社':  
					s3='%'+Stu_query.get()+'%'
					c.execute("SELECT * FROM booklist WHERE publisher LIKE ?",(s3,))
					x3=c.fetchall()
					if(x3==[]):
						table.pack()
						notex3=Toplevel()
						Label(notex3,text='此书不存在').pack()
						ttk.Button(notex3,text='返回',command=notex3.withdraw).pack()
						return
					for x3 in c.execute("SELECT * FROM booklist WHERE publisher LIKE ?",(s3,)):
						table.insert('',0,values=(x3))
				elif Stu_dropdown.get()=='出版年份':                            
					s4='%'+Stu_query.get()+'%' 
					c.execute("SELECT * FROM booklist WHERE year LIKE ?",(s4,))
					x4=c.fetchall()
					if(x4==[]):
						table.pack()
						notex4=Toplevel()
						Label(notex4,text='此书不存在').pack()
						ttk.Button(notex4,text='返回',command=notex4.withdraw).pack()
						return
					for x4 in c.execute("SELECT * FROM booklist WHERE year LIKE ?",(s4,)):
						table.insert('',0,values=(x4))
			table.pack()
		def Stu_windowout():                           #登陆后弹出学生窗口
			global Stu_dropdown
			global Stu_query
			global Stu_borro1                    #查询entry
			global Stu_borro1_dropdown  
			global Stu_f2                        #notebook借还面板
			Stu_window=Toplevel()
			Stu_window.title('学生应用系统')
			self.ima = PhotoImage(file="4.png")
			w2 = self.ima.width()
			h2 = self.ima.height()
			Stu_window.geometry("%dx%d+0+0" % (w2, h2))
			Stu_note=ttk.Notebook(Stu_window)
			Stu_note.pack()
			Stu_f1=Frame(Stu_note)
			bg1=Label(Stu_f1,image=self.ima).pack()
			Stu_f2=Frame(Stu_note)
			bg2=Label(Stu_f2,image=self.ima).pack()
			Stu_note.add(Stu_f1,text='书籍查询')                     #书籍查询页面
			Stu_query = Entry(Stu_f1)   
			Stu_query.place(x=170,y=220,width=500,height=30)
			Stu_query_button = ttk.Button(Stu_f1,text='GO',command=Stu_query_click).place(x=690,y=215,width=70,height=36)		
			Stu_items = ('关键字','作者','出版社','出版年份')
			Stu_dropdown= Pmw.ComboBox(Stu_f1,label_text='请选择',labelpos='nw',scrolledlist_items = Stu_items)   #读者查询的下拉选择菜单选择查询方式
			Stu_dropdown.place(x=50,y=205,width=100)
			fir = Stu_items[0]
			Stu_dropdown.selectitem(fir)

			Stu_note.add(Stu_f2,text='书籍借阅与退还')               #书籍借还页面
			Stu_borro1=Entry(Stu_f2)
			Stu_borro1.place(x=120,y=40,width=200,height=25)
			Stu_borro1_items=('ISBN','索书号')
			Stu_borro1_button=ttk.Button(Stu_f2,text='确定',command=Stu_borro1_click).place(x=330,y=40,width=40,height=30)
			Stu_borro1_dropdown=Pmw.ComboBox(Stu_f2,label_text='请选择',labelpos='nw',scrolledlist_items=Stu_borro1_items)
			Stu_borro1_dropdown.place(x=20,y=40,width=80)
			sec=Stu_borro1_items[1]
			Stu_borro1_dropdown.selectitem(sec)
			
			

			button1 = ttk.Button(Stu_f2,text='借阅',command=Stu_borro2_click).place(x=50,y=450,width=200,height=36)
			button2 = ttk.Button(Stu_f2,text='退还',command=Stu_back_click).place(x=400,y=450,width=200,height=36)

		def Ad_submit():
			global name7
			global name1_entry
			global name2_entry
			global name3_entry
			global name4_entry
			global name5_entry
			global name6_entry
			global name7_entry
			global name8_entry

			
			if (name1_entry.get()=='')or(name2_entry.get()=='')or(name3_entry.get()=='')or(name4_entry.get()=='')or(name5_entry.get()=='')or(name6_entry.get()=='')or(name7_entry.get()=='')or(name8_entry.get()==''):
				confirm=Toplevel()
				Label(confirm,text='数据输入不完整，请重新输入！').pack()
				ttk.Button(confirm,text='返回',command=confirm.withdraw).pack()
				return
			newtime='%Y-%m-%d %X'
			s=time.strftime(newtime,time.localtime())
			s1=name2_entry.get()
			s2=name1_entry.get()
			s3=name3_entry.get()
			s4=name4_entry.get()
			s5=name6_entry.get()
			s6=name5_entry.get()
			s7=name8_entry.get()
			s8=int(name7_entry.get())

			c.execute("INSERT INTO booklist VALUES(?,?,?,?,?,?,'待上架',?,?,0);",(s1,s2,s3,s4,s5,s6,s7,s8))    
			c.execute("INSERT INTO buy VALUES(?,?,?);",(s1,s8,s))
			c.execute('INSERT INTO updatebook VALUES(?,?,0,?)',(s1,s8,s,)) 
			conn.commit()

			success=Toplevel()
			Label(success,text='新书入库成功！').pack()
			ttk.Button(success,text='确定',command=success.withdraw).pack()  

		def buynewbook():
			global Ad_query_table
			global name1_entry
			global name2_entry
			global name3_entry
			global name4_entry
			global name5_entry
			global name6_entry
			global name7_entry
			global name8_entry
			global Ad_f1
			global name7
			name1=Label(Ad_f1,text='书名',font='YaHei 12 bold',compound='center').place(x=20,y=150)
			name1_entry=Entry(Ad_f1)
			name1_entry.place(x=80,y=150,width=600,height=26)

			name2=Label(Ad_f1,text='ISBN',font='YaHei 12 bold',compound='center').place(x=20,y=200)
			name2_entry=Entry(Ad_f1)
			name2_entry.place(x=80,y=200,width=180,height=24)

			name3=Label(Ad_f1,text='索书号',font='YaHei 12 bold',compound='center').place(x=280,y=200)
			name3_entry=Entry(Ad_f1)
			name3_entry.place(x=375,y=200,width=300,height=24)

			name4=Label(Ad_f1,text='作者',font='YaHei 12 bold',compound='center').place(x=20,y=250)
			name4_entry=Entry(Ad_f1)
			name4_entry.place(x=85,y=250,width=300,height=24)

			name5=Label(Ad_f1,text='出版年份',font='YaHei 12 bold',compound='center').place(x=400,y=250)
			name5_entry=Entry(Ad_f1)
			name5_entry.place(x=490,y=250,width=190,height=24)

			name6=Label(Ad_f1,text='出版社',font='YaHei 12 bold',compound='center').place(x=20,y=300)
			name6_entry=Entry(Ad_f1)
			name6_entry.place(x=90,y=300,width=300,height=24)

			name7=Label(Ad_f1,text='可借量',font='YaHei 12 bold',compound='center').place(x=410,y=300)
			name7_entry=Entry(Ad_f1)
			name7_entry.place(x=480,y=300,width=200,height=24)

			name8=Label(Ad_f1,text='藏书地',font='YaHei 12 bold',compound='center').place(x=20,y=350)
			name8_entry=Entry(Ad_f1)
			name8_entry.place(x=90,y=350,width=590,height=24)

			submit_button = ttk.Button(Ad_f1,text='提交',command=Ad_submit).place(x=300,y=430,width=100,height=35)
		

		def Ad_kill():
			global content
			global num_entry
			if(num_entry.get()==''):
				er=Toplevel()
				label=Label(er,text='请输入淘汰书本数量').pack()
				button=ttk.Button(er,text='返回',command=er.withdraw).pack()
				return
			if (int(num_entry.get())==int(content[8])):
				newtime='%Y-%m-%d %X'
				s=time.strftime(newtime,time.localtime())
				c.execute('DELETE FROM booklist WHERE ISBN=?',(content[0],))
				c.execute('INSERT INTO updatebook VALUES (?,0,?,?)',(content[0],content[8],s))
				conn.commit()
				notice=Toplevel()
				notice_label=Label(notice,text='此书将会从数据库中删除').pack()
				notice_button=ttk.Button(notice,text='确定',command=notice.withdraw).pack()
			else:
				s1=int(num_entry.get())
				newtime='%Y-%m-%d %X'
				s=time.strftime(newtime,time.localtime())
				c.execute('INSERT INTO updatebook VALUES (?,0,?,?)',(content[0],s1,s))
				c.execute("UPDATE booklist SET leftnum=leftnum-? WHERE ISBN=?",(s1,content[0],))
				conn.commit()
			success=Toplevel()
			success_label=Label(success,text='书籍淘汰成功！').pack()
			success_button=ttk.Button(success,text='确定',command=success.withdraw).pack()


		def Ad_change():
			global content
			global suoshuhao_entry
			global state_entry
			global place_entry
			global num_entry
			if (state_entry.get()=='')and(suoshuhao_entry.get()=='')and(place_entry.get()=='')and(num_entry.get()==''):
				er=Toplevel()
				label=Label(er,text='请输入更新信息').pack()
				button=ttk.Button(er,text='返回',command=er.withdraw).pack()
				return
			if(suoshuhao_entry.get()!=''):
				s1=suoshuhao_entry.get()
				c.execute("UPDATE booklist SET num=? WHERE ISBN=?",(s1,content[0],))
				conn.commit()
			if(state_entry.get()!=''):
				s2=state_entry.get()
				c.execute("UPDATE booklist SET state=? WHERE ISBN=?",(s2,content[0],))    
				conn.commit()
			if(place_entry.get()!=''):
				s3=place_entry.get()
				c.execute("UPDATE booklist SET place=? WHERE ISBN=?",(s3,content[0],))
				conn.commit()
			if(num_entry.get()!=''):
				newtime='%Y-%m-%d %X'
				s=time.strftime(newtime,time.localtime())
				s4=int(num_entry.get())
				c.execute("UPDATE booklist SET leftnum=leftnum+? WHERE ISBN=?",(s4,content[0],))
				c.execute('INSERT INTO updatebook VALUES(?,?,0,?)',(content[0],s4,s,))
				conn.commit()
			success=Toplevel()
			label_success=Label(success,text='更新成功！').pack()
			button_success=ttk.Button(success,text='确定',command=success.withdraw).pack()


		def updatenew(event):
			global table
			global content
			global suoshuhao_entry
			global state_entry
			global place_entry
			global num_entry
			item = table.selection()[0]
			content=table.item(item,"values")
			update_top=Toplevel()
			update_top.title('书籍更新与淘汰')
			update_top.geometry('400x350')
			name=Label(update_top,text='图书基本信息').place(x=170,y=10)
			name_top=Label(update_top,text='书名:          '+content[1]).place(x=150,y=70)
			suoshuhao_top=Label(update_top,text='索书号: '+content[2]).place(x=50,y=190)
			suoshuhao_entry=Entry(update_top)
			suoshuhao_entry.place(x=220,y=190)
			autor_top=Label(update_top,text='作者:          '+content[3]).place(x=150,y=100)
			publisher_top=Label(update_top,text='出版社:        '+content[4]).place(x=150,y=130)
			state_top=Label(update_top,text='书籍状态: '+content[6]).place(x=50,y=160)
			state_entry=Entry(update_top)
			state_entry.place(x=220,y=160)
			ISBN_top=Label(update_top,text='ISBN:         '+content[0]).place(x=150,y=40)
			num_top=Label(update_top,text='可借量: '+content[8]).place(x=50,y=220)
			num_entry=Entry(update_top)
			num_entry.place(x=220,y=220)
			place_top=Label(update_top,text='藏书地: '+content[7]).place(x=50,y=250)
			place_entry=Entry(update_top)
			place_entry.place(x=220,y=250)
			change= ttk.Button(update_top,text='更新',command=Ad_change)
			change.place(x=100,y=280)
			kill= ttk.Button(update_top,text='淘汰',command=Ad_kill)
			kill.place(x=200,y=280)
		def Ad_query_click():
			global Ad_dropdown
			global Ad_query
			global Ad_query_table
			global table
			Ad_query_table=Toplevel()                        
			Ad_query_table.title('书籍更新')	
			table=ttk.Treeview(Ad_query_table,columns=('col1','col2','col3','col4','col5','col6','col7','col8','col9','col10'))   
			table.column('col1', width=100, anchor='w')  
			table.column('col2', width=180, anchor='w')
			table.column('col3', width=100, anchor='w')
			table.column('col4', width=100, anchor='w')
			table.column('col5', width=150, anchor='w')
			table.column('col6', width=70,  anchor='center')
			table.column('col7', width=120, anchor='w')
			table.column('col8', width=200, anchor='center')
			table.column('col9', width=50, anchor='center')
			table.column('col10', width=50, anchor='center')
			table.heading('col1', text='ISBN')
			table.heading('col2', text='书名')
			table.heading('col3', text='索书号')
			table.heading('col4', text='作者')
			table.heading('col5', text='出版社')
			table.heading('col6', text='出版年份')
			table.heading('col7', text='书籍状态')
			table.heading('col8', text='馆藏地')
			table.heading('col9', text='可借量')
			table.heading('col10', text='借出量')
			if Ad_query.get()=='':
				for z in c.execute("SELECT * FROM booklist"):
					table.insert('',0,values=(z))
				table.bind('<Double-1>',updatenew)
			if Ad_query.get()!='':
				if Ad_dropdown.get()=='关键字':
					s1='%'+Ad_query.get()+'%'
					c.execute("SELECT * FROM booklist WHERE title LIKE ?",(s1,))
					x1=c.fetchall()
					if(x1==[]):
						table.pack()
						notex1=Toplevel()
						Label(notex1,text='此书不存在').pack()
						ttk.Button(notex1,text='返回',command=notex1.withdraw).pack()
						buynewbook()
						return

					for x1 in c.execute("SELECT * FROM booklist WHERE title LIKE ?",(s1,)):
						table.insert('',0,values=(x1))
					table.bind("<Double-1>", updatenew)
					
				elif Ad_dropdown.get()=='作者': 
					s2='%'+Ad_query.get()+'%'
					c.execute("SELECT * FROM booklist WHERE author LIKE ?",(s2,))
					x2=c.fetchall()
					if(x2==[]):
						table.pack()
						notex2=Toplevel()
						Label(notex2,text='此书不存在').pack()
						ttk.Button(notex2,text='返回',command=notex2.withdraw).pack()
						buynewbook()
						return
					for x2 in c.execute("SELECT * FROM booklist WHERE author LIKE ?",(s2,)):
						table.insert('',0,values=(x2))
					table.bind('<Double-1>',updatenew)
				elif Ad_dropdown.get()=='出版社':  
					s3='%'+Ad_query.get()+'%'
					c.execute("SELECT * FROM booklist WHERE publisher LIKE ?",(s3,))
					x3=c.fetchall()
					if(x3==[]):
						table.pack()
						notex3=Toplevel()
						Label(notex3,text='此书不存在').pack()
						ttk.Button(notex3,text='返回',command=notex3.withdraw).pack()
						buynewbook()
						return
					for x3 in c.execute("SELECT * FROM booklist WHERE publisher LIKE ?",(s3,)):
						table.insert('',0,values=(x3))
					table.bind('<Double-1>',updatenew)
				elif Ad_dropdown.get()=='ISBN':                            
					s4='%'+Ad_query.get()+'%' 
					c.execute("SELECT * FROM booklist WHERE ISBN LIKE ?",(s4,))
					x4=c.fetchall()
					if(x4==[]):
						table.pack()
						notex4=Toplevel()
						Label(notex4,text='此书不存在').pack()
						ttk.Button(notex4,text='返回',command=notex4.withdraw).pack()
						buynewbook()
						return
					for x4 in c.execute("SELECT * FROM booklist WHERE ISBN LIKE ?",(s4,)):
						table.insert('',0,values=(x4))
					table.bind('<Double-1>',updatenew)
			table.pack()
		
		
		def Ad_update_query_click1():
			global Ad_update_dropdown1
			global Ad_update_query1
			Ad_query_table1=Toplevel()                        
			Ad_query_table1.title('书籍更新历史查询')
			table= ttk.Treeview(Ad_query_table1,columns=('col1','col2','col3','col4','col5'))   
			table.column('col1', width=100, anchor='w')  
			table.column('col2', width=180, anchor='w')
			table.column('col3', width=100, anchor='w')
			table.column('col4', width=100, anchor='w')
			table.column('col5', width=150, anchor='w')
			table.heading('col1', text='ISBN')
			table.heading('col2', text='书名')
			table.heading('col3', text='新入数量')
			table.heading('col4', text='淘汰数量')
			table.heading('col5', text='更新时间')
			if Ad_update_query1.get()=='':
				for z in c.execute("SELECT booklist.ISBN,booklist.title,updatebook.newnum,updatebook.dienum,updatebook.updatetime FROM booklist,updatebook WHERE booklist.ISBN=updatebook.ISBN"):
					table.insert('',0,values=(z))
			if Ad_update_query1.get()!='':
				if Ad_update_dropdown1.get()=='关键字':
					s1='%'+Ad_update_query1.get()+'%'
					c.execute("SELECT booklist.ISBN,booklist.title,updatebook.newnum,updatebook.dienum,updatebook.updatetime FROM booklist,updatebook WHERE booklist.ISBN=updatebook.ISBN and title LIKE ?",(s1,))
					x1=c.fetchall()
					if(x1==[]):
						table.pack()
						notex1=Toplevel()
						Label(notex1,text='此书不存在').pack()
						ttk.Button(notex1,text='返回',command=notex1.withdraw).pack()
						return
					for x1 in c.execute("SELECT booklist.ISBN,booklist.title,updatebook.newnum,updatebook.dienum,updatebook.updatetime FROM booklist,updatebook WHERE booklist.ISBN=updatebook.ISBN and title LIKE ?",(s1,)):
						table.insert('',0,values=(x1))
				elif Ad_update_dropdown1.get()=='作者': 
					s2='%'+Ad_update_query1.get()+'%'
					c.execute("SELECT booklist.ISBN,booklist.title,updatebook.newnum,updatebook.dienum,updatebook.updatetime FROM booklist,updatebook WHERE booklist.ISBN=updatebook.ISBN and author LIKE ?",(s2,))
					x2=c.fetchall()
					if(x2==[]):
						table.pack()
						notex2=Toplevel()
						Label(notex2,text='此书不存在').pack()
						ttk.Button(notex2,text='返回',command=notex2.withdraw).pack()
						return
					for x2 in c.execute("SELECT booklist.ISBN,booklist.title,updatebook.newnum,updatebook.dienum,updatebook.updatetime FROM booklist,updatebook WHERE booklist.ISBN=updatebook.ISBN and author LIKE ?",(s2,)):
						table.insert('',0,values=(x2))
				elif Ad_update_dropdown1.get()=='出版社':  
					s3='%'+Ad_update_query1.get()+'%'
					c.execute("SELECT booklist.ISBN,booklist.title,updatebook.newnum,updatebook.dienum,updatebook.updatetime FROM booklist,updatebook WHERE booklist.ISBN=updatebook.ISBN and publisher LIKE ?",(s3,))
					x3=c.fetchall()
					if(x3==[]):
						table.pack()
						notex3=Toplevel()
						Label(notex3,text='此书不存在').pack()
						ttk.Button(notex3,text='返回',command=notex3.withdraw).pack()
						return
					for x3 in c.execute("SELECT booklist.ISBN,booklist.title,updatebook.newnum,updatebook.dienum,updatebook.updatetime FROM booklist,updatebook WHERE booklist.ISBN=updatebook.ISBN and publisher LIKE ?",(s3,)):
						table.insert('',0,values=(x3))
				elif Ad_update_dropdown1.get()=='出版年份':                            
					s4='%'+Ad_update_query1.get()+'%' 
					c.execute("SELECT booklist.ISBN,booklist.title,updatebook.newnum,updatebook.dienum,updatebook.updatetime FROM booklist,updatebook WHERE booklist.ISBN=updatebook.ISBN and year LIKE ?",(s4,))
					x4=c.fetchall()
					if(x4==[]):
						table.pack()
						notex4=Toplevel()
						Label(notex4,text='此书不存在').pack()
						ttk.Button(notex4,text='返回',command=notex4.withdraw).pack()
						return
					for x4 in c.execute("SELECT booklist.ISBN,booklist.title,updatebook.newnum,updatebook.dienum,updatebook.updatetime FROM booklist,updatebook WHERE booklist.ISBN=updatebook.ISBN and year LIKE ?",(s4,)):
						table.insert('',0,values=(x4))
			table.pack()

		def Ad_update_query_click2():
			global Ad_update_dropdown2
			global Ad_update_query2
			Ad_query_table1=Toplevel()                        
			Ad_query_table1.title('书籍借阅历史查询')
			table= ttk.Treeview(Ad_query_table1,columns=('col1','col2','col3','col4','col5','col6'))   
			table.column('col1', width=100, anchor='w')  
			table.column('col2', width=180, anchor='w')
			table.column('col3', width=100, anchor='w')
			table.column('col4', width=100, anchor='w')
			table.column('col5', width=150, anchor='w')
			table.column('col6', width=150, anchor='w')
			table.heading('col1', text='ISBN')
			table.heading('col2', text='书名')
			table.heading('col3', text='持有人ID')
			table.heading('col4', text='持有人姓名')
			table.heading('col5', text='借阅时间')
			table.heading('col6', text='返还时间')
			if Ad_update_query2.get()=='':
				for z in c.execute("SELECT borrow.ISBN,booklist.title,Readerlist.ReaderID,Readerlist.Name,borrow.borrowtime,borrow.returntime FROM borrow,booklist,Readerlist WHERE borrow.ISBN=booklist.ISBN and borrow.ReaderID=Readerlist.ReaderID"):
					table.insert('',0,values=(z))
			if Ad_update_query2.get()!='':
				if Ad_update_dropdown2.get()=='关键字':
					s1='%'+Ad_update_query2.get()+'%'
					c.execute("SELECT borrow.ISBN,booklist.title,Readerlist.ReaderID,Readerlist.Name,borrow.borrowtime,borrow.returntime FROM borrow,booklist,Readerlist WHERE borrow.ISBN=booklist.ISBN and borrow.ReaderID=Readerlist.ReaderID and booklist.title LIKE ?",(s1,))
					x1=c.fetchall()
					if(x1==[]):
						table.pack()
						notex1=Toplevel()
						Label(notex1,text='此书不存在').pack()
						ttk.Button(notex1,text='返回',command=notex1.withdraw).pack()
						return
					for x1 in c.execute("SELECT borrow.ISBN,booklist.title,Readerlist.ReaderID,Readerlist.Name,borrow.borrowtime,borrow.returntime FROM borrow,booklist,Readerlist WHERE borrow.ISBN=booklist.ISBN and borrow.ReaderID=Readerlist.ReaderID and booklist.title LIKE ?",(s1,)):
						table.insert('',0,values=(x1))
				elif Ad_update_dropdown2.get()=='作者': 
					s2='%'+Ad_update_query2.get()+'%'
					c.execute("SELECT borrow.ISBN,booklist.title,Readerlist.ReaderID,Readerlist.Name,borrow.borrowtime,borrow.returntime FROM borrow,booklist,Readerlist WHERE borrow.ISBN=booklist.ISBN and borrow.ReaderID=Readerlist.ReaderID and booklist.author LIKE ?",(s2,))
					x2=c.fetchall()
					if(x2==[]):
						table.pack()
						notex2=Toplevel()
						Label(notex2,text='此书不存在').pack()
						ttk.Button(notex2,text='返回',command=notex2.withdraw).pack()
						return
					for x2 in c.execute("SELECT borrow.ISBN,booklist.title,Readerlist.ReaderID,Readerlist.Name,borrow.borrowtime,borrow.returntime FROM borrow,booklist,Readerlist WHERE borrow.ISBN=booklist.ISBN and borrow.ReaderID=Readerlist.ReaderID and booklist.author LIKE ?",(s2,)):
						table.insert('',0,values=(x2))
				elif Ad_update_dropdown2.get()=='出版社':  
					s3='%'+Ad_update_query2.get()+'%'
					c.execute("SELECT borrow.ISBN,booklist.title,Readerlist.ReaderID,Readerlist.Name,borrow.borrowtime,borrow.returntime FROM borrow,booklist,Readerlist WHERE borrow.ISBN=booklist.ISBN and borrow.ReaderID=Readerlist.ReaderID and booklist.publisher LIKE ?",(s3,))
					x3=c.fetchall()
					if(x3==[]):
						table.pack()
						notex3=Toplevel()
						Label(notex3,text='此书不存在').pack()
						ttk.Button(notex3,text='返回',command=notex3.withdraw).pack()
						return
					for x3 in c.execute("SELECT borrow.ISBN,booklist.title,Readerlist.ReaderID,Readerlist.Name,borrow.borrowtime,borrow.returntime FROM borrow,booklist,Readerlist WHERE borrow.ISBN=booklist.ISBN and borrow.ReaderID=Readerlist.ReaderID and booklist.publisher LIKE ?",(s3,)):
						table.insert('',0,values=(x3))
				elif Ad_update_dropdown2.get()=='出版年份':                            
					s4='%'+Ad_update_query2.get()+'%' 
					c.execute("SELECT borrow.ISBN,booklist.title,Readerlist.ReaderID,Readerlist.Name,borrow.borrowtime,borrow.returntime FROM borrow,booklist,Readerlist WHERE borrow.ISBN=booklist.ISBN and borrow.ReaderID=Readerlist.ReaderID and booklist.year LIKE ?",(s4,))
					x4=c.fetchall()
					if(x4==[]):
						table.pack()
						notex4=Toplevel()
						Label(notex4,text='此书不存在').pack()
						ttk.Button(notex4,text='返回',command=notex4.withdraw).pack()
						return
					for x4 in c.execute("SELECT borrow.ISBN,booklist.title,Readerlist.ReaderID,Readerlist.Name,borrow.borrowtime,borrow.returntime FROM borrow,booklist,Readerlist WHERE borrow.ISBN=booklist.ISBN and borrow.ReaderID=Readerlist.ReaderID and booklist.year LIKE ?",(s4,)):
						table.insert('',0,values=(x4))
				elif Ad_update_dropdown2.get()=='读者ID':                            
					s5='%'+Ad_update_query2.get()+'%' 
					c.execute("SELECT borrow.ISBN,booklist.title,Readerlist.ReaderID,Readerlist.Name,borrow.borrowtime,borrow.returntime FROM borrow,booklist,Readerlist WHERE borrow.ISBN=booklist.ISBN and borrow.ReaderID=Readerlist.ReaderID and Readerlist.ReaderID LIKE ?",(s5,))
					x5=c.fetchall()
					if(x5==[]):
						table.pack()
						notex5=Toplevel()
						Label(notex5,text='此书不存在').pack()
						ttk.Button(notex5,text='返回',command=notex5.withdraw).pack()
						return
					for x5 in c.execute("SELECT borrow.ISBN,booklist.title,Readerlist.ReaderID,Readerlist.Name,borrow.borrowtime,borrow.returntime FROM borrow,booklist,Readerlist WHERE borrow.ISBN=booklist.ISBN and borrow.ReaderID=Readerlist.ReaderID and Readerlist.ReaderID LIKE ?",(s5,)):
						table.insert('',0,values=(x5))
				elif Ad_update_dropdown2.get()=='读者姓名':                            
					s6='%'+Ad_update_query2.get()+'%' 
					c.execute("SELECT borrow.ISBN,booklist.title,Readerlist.ReaderID,Readerlist.Name,borrow.borrowtime,borrow.returntime FROM borrow,booklist,Readerlist WHERE borrow.ISBN=booklist.ISBN and borrow.ReaderID=Readerlist.ReaderID and Readerlist.Name LIKE ?",(s6,))
					x6=c.fetchall()
					if(x6==[]):
						table.pack()
						notex6=Toplevel()
						Label(notex6,text='此书不存在').pack()
						ttk.Button(notex6,text='返回',command=notex6.withdraw).pack()
						return
					for x6 in c.execute("SELECT borrow.ISBN,booklist.title,Readerlist.ReaderID,Readerlist.Name,borrow.borrowtime,borrow.returntime FROM borrow,booklist,Readerlist WHERE borrow.ISBN=booklist.ISBN and borrow.ReaderID=Readerlist.ReaderID and Readerlist.Name LIKE ?",(s6,)):
						table.insert('',0,values=(x6))
			table.pack()
		def Ad_update_query_click3():
			global Ad_update_dropdown3
			global Ad_update_query3
			Ad_query_table1=Toplevel()                        
			Ad_query_table1.title('读者信息查询')
			table= ttk.Treeview(Ad_query_table1,columns=('col1','col2','col3','col4','col5','col6','col7'))   
			table.column('col1', width=100, anchor='w')  
			table.column('col2', width=180, anchor='w')
			table.column('col3', width=100, anchor='w')
			table.column('col4', width=100, anchor='w')
			table.column('col5', width=150, anchor='w')
			table.column('col6', width=150, anchor='w')
			table.column('col7', width=150, anchor='w')
			table.heading('col1', text='读者ID')
			table.heading('col2', text='读者姓名')
			table.heading('col3', text='性别')
			table.heading('col4', text='学院')
			table.heading('col5', text='所持书目ID')
			table.heading('col6', text='所持书目名称')
			table.heading('col7', text='借阅时间')
			if Ad_update_query3.get()=='':
				for z in c.execute("SELECT Readerlist.ReaderID,Readerlist.Name,Readerlist.Sex,Readerlist.Department,borrow.ISBN,booklist.title,borrow.borrowtime FROM booklist,borrow,Readerlist WHERE booklist.ISBN=borrow.ISBN and Readerlist.ReaderID=borrow.ReaderID and borrow.borrowtime<>'-'"):
					table.insert('',0,values=(z))
			if Ad_update_query3.get()!='':
				if Ad_update_dropdown3.get()=='读者ID':
					s1='%'+Ad_update_query3.get()+'%'
					c.execute("SELECT Readerlist.ReaderID,Readerlist.Name,Readerlist.Sex,Readerlist.Department,borrow.ISBN,booklist.title,borrow.borrowtime FROM booklist,borrow,Readerlist WHERE booklist.ISBN=borrow.ISBN and Readerlist.ReaderID=borrow.ReaderID and borrow.borrowtime<>'-' and Readerlist.ReaderID LIKE ?",(s1,))
					x1=c.fetchall()
					if(x1==[]):
						table.pack()
						notex1=Toplevel()
						Label(notex1,text='此书不存在').pack()
						ttk.Button(notex1,text='返回',command=notex1.withdraw).pack()
						return
					for x1 in c.execute("SELECT Readerlist.ReaderID,Readerlist.Name,Readerlist.Sex,Readerlist.Department,borrow.ISBN,booklist.title,borrow.borrowtime FROM booklist,borrow,Readerlist WHERE booklist.ISBN=borrow.ISBN and Readerlist.ReaderID=borrow.ReaderID and borrow.borrowtime<>'-' and Readerlist.ReaderID LIKE ?",(s1,)):
						table.insert('',0,values=(x1))
				elif Ad_update_dropdown3.get()=='姓名': 
					s2='%'+Ad_update_query3.get()+'%'
					c.execute("SELECT Readerlist.ReaderID,Readerlist.Name,Readerlist.Sex,Readerlist.Department,borrow.ISBN,booklist.title,borrow.borrowtime FROM booklist,borrow,Readerlist WHERE booklist.ISBN=borrow.ISBN and Readerlist.ReaderID=borrow.ReaderID and borrow.borrowtime<>'-' and Readerlist.Name LIKE ?",(s2,))
					x2=c.fetchall()
					if(x2==[]):
						table.pack()
						notex2=Toplevel()
						Label(notex2,text='此书不存在').pack()
						ttk.Button(notex2,text='返回',command=notex2.withdraw).pack()
						return
					for x2 in c.execute("SELECT Readerlist.ReaderID,Readerlist.Name,Readerlist.Sex,Readerlist.Department,borrow.ISBN,booklist.title,borrow.borrowtime FROM booklist,borrow,Readerlist WHERE booklist.ISBN=borrow.ISBN and borrow.borrowtime<>'-' and Readerlist.ReaderID=borrow.ReaderID and Readerlist.Name LIKE ?",(s2,)):
						table.insert('',0,values=(x2))
				elif Ad_update_dropdown3.get()=='学院':  
					s3='%'+Ad_update_query3.get()+'%'
					c.execute("SELECT Readerlist.ReaderID,Readerlist.Name,Readerlist.Sex,Readerlist.Department,borrow.ISBN,booklist.title,borrow.borrowtime FROM booklist,borrow,Readerlist WHERE booklist.ISBN=borrow.ISBN and Readerlist.ReaderID=borrow.ReaderID and borrow.borrowtime<>'-' and Readerlist.Department LIKE ?",(s3,))
					x3=c.fetchall()
					if(x3==[]):
						table.pack()
						notex3=Toplevel()
						Label(notex3,text='此书不存在').pack()
						ttk.Button(notex3,text='返回',command=notex3.withdraw).pack()
						return
					for x3 in c.execute("SELECT Readerlist.ReaderID,Readerlist.Name,Readerlist.Sex,Readerlist.Department,borrow.ISBN,booklist.title,borrow.borrowtime FROM booklist,borrow,Readerlist WHERE booklist.ISBN=borrow.ISBN and Readerlist.ReaderID=borrow.ReaderID and borrow.borrowtime<>'-' and Readerlist.Department LIKE ?",(s3,)):
						table.insert('',0,values=(x3))
			table.pack()

		def statistics1():
			c.execute('SELECT sum(leftnum) FROM booklist')
			s=c.fetchall()[0][0]
			s1=str(s)
			c.execute('SELECT sum(borrowed) FROM booklist')
			ss=c.fetchall()[0][0]
			s2=str(ss)
			sss=s+ss
			s3=str(sss)
			x=Toplevel()
			x.title('库存数目统计')
			x_label1=Label(x,text='目前库存共'+s3+'本').place(x=50,y=20)
			x_label2=Label(x,text='已借出'+s2+'本').place(x=50,y=50)
			x_label3=Label(x,text='未借出'+s1+'本').place(x=50,y=80)
			x_button=ttk.Button(x,text='确定',command=x.withdraw).place(x=55,y=130)
		def statistics2():
			c.execute('SELECT sum(num) FROM buy')
			s=c.fetchall()[0][0]
			s1=str(s)
			c.execute('SELECT sum(newnum) FROM updatebook')
			ss=c.fetchall()[0][0]
			s2=str(ss)
			sss=s+ss
			s3=str(sss)
			x=Toplevel()
			x.title('更新数目统计')
			x_label1=Label(x,text='目前共新入库'+s3+'本').place(x=50,y=20)
			x_label2=Label(x,text='更新入库'+s2+'本').place(x=50,y=50)
			x_label3=Label(x,text='新购入库'+s1+'本').place(x=50,y=80)
			x_button=ttk.Button(x,text='确定',command=x.withdraw).place(x=55,y=130)
		def statistics3():
			c.execute('SELECT sum(dienum) FROM updatebook')
			s=c.fetchall()[0][0]
			s1=str(s)
			x=Toplevel()
			x.title('淘汰数目统计')
			x_label1=Label(x,text='目前共淘汰'+s1+'本').place(x=50,y=50)
			x_button=ttk.Button(x,text='确定',command=x.withdraw).place(x=55,y=130)
		def statistics4():
			c.execute('SELECT count(distinct ReaderID) FROM Readerlist')
			s=c.fetchall()[0][0]
			s1=str(s)
			x=Toplevel()
			x.title('读者数目统计')
			x_label1=Label(x,text='目前共有注册读者'+s1+'人').place(x=50,y=50)
			x_button=ttk.Button(x,text='确定',command=x.withdraw).place(x=55,y=130)
		def Ad_managerfun():
			global ISBN_entry
			global Ad_f1
			global Ad_dropdown
			global Ad_query
			global Ad_update_query1
			global Ad_update_dropdown1
			global Ad_update_query2
			global Ad_update_dropdown2
			global Ad_update_query3
			global Ad_update_dropdown3
			Ad_manager=Toplevel()
			Ad_manager.title('管理员应用系统')
			self.imag = PhotoImage(file="4.png")
			w22 = self.imag.width()
			h11=self.imag.height()
			Ad_manager.geometry("%dx%d+0+0" % (w22, h11))
			Ad_note1=ttk.Notebook(Ad_manager)
			Ad_note1.pack()
			Ad_f1=Frame(Ad_note1)
			bg1=Label(Ad_f1,image=self.imag).pack()
			Ad_f2=Frame(Ad_note1)
			bg2=Label(Ad_f2,image=self.imag).pack()
			Ad_f3=Frame(Ad_note1)
			bg3=Label(Ad_f3,image=self.imag).pack()
			Ad_f4=Frame(Ad_note1)
			bg4=Label(Ad_f4,image=self.imag).pack()
			Ad_f5=Frame(Ad_note1)
			bg5=Label(Ad_f5,image=self.imag).pack()
			Ad_note1.add(Ad_f1,text='书籍更新')
			Ad_query = Entry(Ad_f1)   
			Ad_query.place(x=170,y=50,width=200,height=30)
			Ad_query_button = ttk.Button(Ad_f1,text='GO',command=Ad_query_click).place(x=390,y=50,width=50,height=28)		
			Ad_items = ('关键字','作者','出版社','ISBN')
			Ad_dropdown= Pmw.ComboBox(Ad_f1,label_text='请选择',labelpos='nw',scrolledlist_items = Ad_items)  
			Ad_dropdown.place(x=50,y=50,width=100)
			Ad_fir = Ad_items[3]
			Ad_dropdown.selectitem(Ad_fir)
			

			Ad_note1.add(Ad_f2,text='书籍更新历史查询')
			Ad_update_query1 = Entry(Ad_f2)   
			Ad_update_query1.place(x=170,y=220,width=500,height=30)
			Ad_update_button1 = ttk.Button(Ad_f2,text='GO',command=Ad_update_query_click1).place(x=690,y=215,width=70,height=36)		
			Ad_update_items1 = ('关键字','作者','出版社','出版年份')
			Ad_update_dropdown1= Pmw.ComboBox(Ad_f2,label_text='请选择',labelpos='nw',scrolledlist_items = Ad_update_items1)   
			Ad_update_dropdown1.place(x=50,y=205,width=100)
			Ad_update_fir1 = Ad_update_items1[0]
			Ad_update_dropdown1.selectitem(Ad_update_fir1)


			Ad_note1.add(Ad_f3,text='借阅历史查询')
			Ad_update_query2 = Entry(Ad_f3)   
			Ad_update_query2.place(x=170,y=220,width=500,height=30)
			Ad_update_button2 = ttk.Button(Ad_f3,text='GO',command=Ad_update_query_click2).place(x=690,y=215,width=70,height=36)		
			Ad_update_items2 = ('关键字','作者','出版社','出版年份','读者ID','读者姓名')
			Ad_update_dropdown2= Pmw.ComboBox(Ad_f3,label_text='请选择',labelpos='nw',scrolledlist_items = Ad_update_items2)  
			Ad_update_dropdown2.place(x=50,y=205,width=100)
			Ad_update_fir2 = Ad_update_items2[0]
			Ad_update_dropdown2.selectitem(Ad_update_fir2)

			Ad_note1.add(Ad_f4,text='读者信息查询')
			Ad_update_query3 = Entry(Ad_f4)   
			Ad_update_query3.place(x=170,y=220,width=500,height=30)
			Ad_update_button3 = ttk.Button(Ad_f4,text='GO',command=Ad_update_query_click3).place(x=690,y=215,width=70,height=36)		
			Ad_update_items3 = ('读者ID','姓名','学院')
			Ad_update_dropdown3= Pmw.ComboBox(Ad_f4,label_text='请选择',labelpos='nw',scrolledlist_items = Ad_update_items3)  
			Ad_update_dropdown3.place(x=50,y=205,width=100)
			Ad_update_fir3 = Ad_update_items3[0]
			Ad_update_dropdown3.selectitem(Ad_update_fir3)

			Ad_note1.add(Ad_f5,text='相关信息统计')
			kucun=ttk.Button(Ad_f5,text='库存数目统计',command=statistics1)
			kucun.place(x=80,y=70,width=150,height=50)
			gengxin=ttk.Button(Ad_f5,text='更新数目统计',command=statistics2)
			gengxin.place(x=450,y=70,width=150,height=50)
			taotai=ttk.Button(Ad_f5,text='淘汰数目统计',command=statistics3)
			taotai.place(x=80,y=350,width=150,height=50)
			jieyue=ttk.Button(Ad_f5,text='读者人数统计',command=statistics4)
			jieyue.place(x=450,y=350,width=150,height=50)
		def Ad_permission():
			global pas_entry
			global IDstring
			if pas_entry.get()=='':
				blank=Toplevel()
				Label(blank,text='请输入密码').pack()
				ttk.Button(blank,text='确定',command=blank.withdraw).pack()
				return
			for x in c.execute("SELECT * FROM Adlist WHERE AdID LIKE ?",(IDstring,)):
				pasget=x[4]
			if (pas_entry.get()!='')and(pas_entry.get()==x[4]):
				Ad_managerfun()
				
			if (pas_entry.get()!='')and(pas_entry.get()!=x[4]):
				paserror=Toplevel()
				Label(paserror,text='密码不正确，请重新输入！').pack()
				ttk.Button(paserror,text='确定',command=paserror.withdraw).pack()
				return
		def changepas():
			global IDstring
			global entry1
			global entry2
			global entry3
			if ((entry1.get()=='')or(entry2.get()=='')or(entry3.get()=='')):
				error1=Toplevel()
				Label(error1,text='请完整输入').pack()
				ttk.Button(error1,text='确定',command=error1.withdraw).pack()
				return				
			for x in c.execute("SELECT * FROM Adlist WHERE AdID LIKE ?",(IDstring,)):
				pasget=x[4]
			if(entry1.get()!=pasget):
				error2=Toplevel()
				Label(error2,text='原密码不正确').pack()
				ttk.Button(error2,text='确定',command=error2.withdraw).pack()
				return
			if(entry2.get()!=entry3.get()):
				error3=Toplevel()
				Label(error3,text='新密码不一致').pack()
				ttk.Button(error3,text='确定',command=error3.withdraw).pack()
				return
			s1=entry3.get()
			c.execute("UPDATE Adlist SET password=? WHERE AdID=?",(s1,IDstring))
			conn.commit()
			error4=Toplevel()
			Label(error4,text='更改成功！').pack()
			ttk.Button(error4,text='确定',command=error4.withdraw).pack()
		def pas_back():
			global entry1
			global entry2
			global entry3
			pasback=Toplevel()
			pasback.title('密码找回')
			self.im=PhotoImage(file='3.png')
			pasback1=Label(pasback,image=self.im)
			w = self.im.width()
			h=self.im.height()
			pasback.geometry("%dx%d+0+0" % (w, h))
			pasback1.pack()
			label1=Label(pasback,text='原密码',font='YaHei 12 bold',compound='center')
			label1.place(x=50,y=100)
			label2=Label(pasback,text='新密码',font='YaHei 12 bold',compound='center')
			label2.place(x=50,y=150)
			label3=Label(pasback,text='新密码确认',font='YaHei 12 bold',compound='center')
			label3.place(x=35,y=200)
			entry1=Entry(pasback)
			entry1.place(x=130,y=100,width=200,height=25)
			entry1['show']='*'
			entry2=Entry(pasback)
			entry2.place(x=130,y=150,width=200,height=25)
			entry2['show']='*'
			entry3=Entry(pasback)
			entry3.place(x=130,y=200,width=200,height=25)
			entry3['show']='*'
			button=ttk.Button(pasback,text='更改',command=changepas)
			button.place(x=160,y=250)
		def Ad_windowout():                            #管理员登陆界面
			global IDstring
			global pas_entry
			Ad_window=Toplevel()
			Ad_window.title('管理员登陆')
			self.ima2 = PhotoImage(file="3.png")
			window2=Label(Ad_window,image=self.ima2)
			w2 = self.ima2.width()
			h1=self.ima2.height()
			Ad_window.geometry("%dx%d+0+0" % (w2, h1))
			window2.pack()
			password=Label(Ad_window,text='密码',font='YaHei 12 bold',compound='center')
			password.place(x=50,y=150)
			ID_label=Label(Ad_window,text='ID',font='YaHei 12 bold',compound='center')
			ID_label.place(x=50,y=100)
			e=StringVar()
			ID_entry=Entry(Ad_window,textvariable = e)
			e.set(IDstring)
			ID_entry.place(x=130,y=100,width=200,height=25)
			ID_entry['state']='readonly'
			pas_entry=Entry(Ad_window)
			pas_entry.place(x=130,y=150,width=200,height=25)
			pas_entry['show']='*'
			pas_button=ttk.Button(Ad_window,text='登陆',command=Ad_permission).place(x=110,y=200)
			pas_back_button=ttk.Button(Ad_window,text='找回密码',command=pas_back).place(x=220,y=200)




		IDstring=enter_ID.get()
		if(enter_ID.get()=='')and(Stu_rbs==1):                            #Ad、Stu登陆判断与窗口弹出
			error1=Toplevel()
			Label(error1,text='请输入ID').pack()
			ttk.Button(error1,text='确定',command=error1.withdraw).pack()
			return
		if(enter_ID.get()=='')and(Ad_rbs==2):
			error2=Toplevel()
			Label(error2,text='请输入ID').pack()
			ttk.Button(error2,text='确定',command=error2.withdraw).pack()
			return
		if(enter_ID.get()=='')and(Ad_rbs==0)and(Stu_rbs==0):
			error4=Toplevel()
			Label(error4,text='请输入ID并且选择角色').pack()
			ttk.Button(error4,text='确定',command=error4.withdraw).pack()
			return
		if(enter_ID.get()!='')and(Ad_rbs==0)and(Stu_rbs==0):
			error3=Toplevel()
			Label(error3,text='请选择角色').pack()
			ttk.Button(error3,text='确定',command=error3.withdraw).pack()
			return
		if(enter_ID.get()!='')and(Ad_rbs==2):
			for AdNum in c.execute('SELECT AdID FROM Adlist'):
				pass
				for y in AdNum:
					if y==enter_ID.get():
						key2=True
			if (key2==False):
				exe2=Toplevel()
				Label(exe2,text='ID不存在，请重新输入').pack()
				ttk.Button(exe2,text='确定',command=exe2.withdraw).pack()
				return
			Ad_windowout()
			
		if(enter_ID.get()!='')and(Stu_rbs==1):                            #学生应用界面，分为查询与借还书两个板块
			for ReaderNum in c.execute('SELECT ReaderID FROM Readerlist'):
				pass
				for x in ReaderNum:
					if x==enter_ID.get():
						key1=True
						break
			if (key1==False):
				exe1=Toplevel()
				Label(exe1,text='ID不存在，请重新输入').pack()
				ttk.Button(exe1,text='确定',command=exe1.withdraw).pack()
				return
			Stu_windowout()
		




	

		


root=Tk()
Pmw.initialise(root)
root.title("中国科学技术大学图书管理系统")
app=Application(root)
app.mainloop()
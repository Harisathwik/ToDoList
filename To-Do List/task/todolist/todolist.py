from sqlalchemy import create_engine

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

while True:
    print("\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    week_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    a = input()
    if a == '1':
        print("\nToday {} {}:".format(datetime.today().day, datetime.today().strftime("%b")))
        rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            for each in range(len(rows)):
                print("{}. {}".format(each + 1, rows[each]))
    elif a == '2':
        today = datetime.today()
        for day in range(0, 7):
            task_date = today.date() + timedelta(days=day)
            rows = session.query(Table).filter(Table.deadline == task_date).all()
            print("\n{} {} {}:".format(week_day[task_date.weekday()], task_date.day, task_date.strftime('%b')))
            if len(rows) == 0:
                print("Nothing to do!")
            else:
                for each in range(len(rows)):
                    print("{}. {}".format(each + 1, rows[each]))
    elif a == '3':
        rows = session.query(Table).order_by(Table.deadline).all()
        print("\nAll tasks:")
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            days = session.query(Table).all()
            for each in range(len(rows)):
                print("{}. {}. {} {}".format(each + 1, rows[each],
                                             rows[each].deadline.day, rows[each].deadline.strftime('%b')))
    elif a == '4':
        print("\nMissed Tasks:")
        rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
        if len(rows) == 0:
            print("Nothing is missed!")
        else:
            for each in range(len(rows)):
                print("{}. {}. {} {}".format(each + 1, rows[each], rows[each].deadline.day,
                                             rows[each].deadline.strftime('%b')))
    elif a == '5':
        print("\nEnter task")
        b = input()
        print("Enter deadline")
        d = input()
        new_row = Table(task=b, deadline=datetime.strptime(d, '%Y-%m-%d').date())
        session.add(new_row)
        session.commit()
        print("The task has been added!")
    elif a == '6':
        rows = session.query(Table).all()
        if len(rows) == 0:
            print("Nothing to delete")
        else:
            print("\nChoose the number of the task you want to delete:")
            for each in range(len(rows)):
                print("{}. {}. {} {}".format(each + 1, rows[each], rows[each].deadline.day,
                                             rows[each].deadline.strftime('%b')))
            a = input()
            print("The task has been deleted!")
            session.query(Table).filter(Table.id == a).delete()
            session.commit()
    elif a == '0':
        print("\nBye!")
        break

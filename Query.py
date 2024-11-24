import mysql.connector
conn=mysql.connector.connect(
    host='localhost',
    user='root',
    password='Zohaib123',
    db='squirrel'
)
c=conn.cursor()


def runQuery():
    print(f'Which query should I run:\n'
          f'1. Squirrel Population based on Observation Site(10,000 sq. meter)\n'
          f'2. Squirrel Behavior by time\n'
          f'3. Observed Primary Fur Color of Squirrels\n'
          f'4. Behavior by Age Group\n'
          f'5. Observed Behavior of Squirrels near Humans\n')
    choice = int(input('Your Choice: '))

    if choice == 1:
        population()
    elif choice == 2:
        activity()
    elif choice == 3:
        furColor()
    elif choice == 4:
        ageBehavior()
    elif choice == 5:
        humanObservedBehavior()


def population():
    query = """
    SELECT Hectare, COUNT(DISTINCT `UniqueSquirrelID`) AS count
    FROM squirreldata
    GROUP BY Hectare
    ORDER BY count DESC;
    """
    c.execute(query)
    info=c.fetchall()
    print(f'\nSquirrel Population based on Observation Site(10,000 sq. meter):')
    print(f'\nObservation Site\tSquirrel Population')
    print('-' * 40)
    for i in info:
        print(f'{i[0]:^16}{i[1]:^25}')

    c.close()
    conn.close()



def activity():
    query = """
    SELECT Shift,
           SUM(CASE WHEN Running = 'true' THEN 1 ELSE 0 END),
           SUM(CASE WHEN Foraging = 'true' THEN 1 ELSE 0 END),
           SUM(CASE WHEN Chasing = 'true' THEN 1 ELSE 0 END),
           SUM(CASE WHEN Climbing = 'true' THEN 1 ELSE 0 END),
           SUM(CASE WHEN Eating = 'true' THEN 1 ELSE 0 END),
           SUM(CASE WHEN OtherActivities IS NOT NULL THEN 1 ELSE 0 END)
    FROM squirreldata
    GROUP BY shift
    ORDER BY shift;
    """
    c.execute(query)
    info = c.fetchall()
    print(f'\nSquirrel Behavior by time:')
    print(f'\nTime\t\tRunning Squirrels\t\tForaging Squirrels\t\tChasing Squirrels'
          f'\t\tClimbing Squirrels\t\tEating Squrriels\t\tOther')
    print('-' * 138)
    for i in info:
        print(f'{i[0]:^4}{i[1]:^32}{i[2]:^18}{i[3]:^29}{i[4]:^20}{i[5]:^25}{i[6]:^15}')

    c.close()
    conn.close()



def furColor():
    query = """
    SELECT CASE
           WHEN PrimaryFurColor = '' THEN 'Other'
           ELSE PrimaryFurColor
       END,
       COUNT(*) AS count
    FROM squirreldata
    GROUP BY PrimaryFurColor
    ORDER BY count DESC;
    """
    c.execute(query)
    info = c.fetchall()
    print(f'\nObserved Primary Fur Color of Squirrels:')
    print(f'\nPrimary Fur Color\t\t\tCount')
    print('-' * 35)
    for i in info:
        print(f'{i[0]:^20}{i[1]:>12}')

    c.close()
    conn.close()



def ageBehavior():
    query = """
    SELECT 
        COALESCE(NULLIF(Age, ''), 'Unknown') AS Age,
        SUM(CASE WHEN Running = 'true' THEN 1 ELSE 0 END),
        SUM(CASE WHEN Chasing = 'true' THEN 1 ELSE 0 END),
        SUM(CASE WHEN Climbing = 'true' THEN 1 ELSE 0 END),
        SUM(CASE WHEN Foraging = 'true' THEN 1 ELSE 0 END)
    FROM squirreldata
    GROUP BY Age
    ORDER BY Age;
    """
    c.execute(query)
    info = c.fetchall()
    print(f'\nBehavior by Age Group:')
    print(f'\nAge Group\t\tRunning\t\tChasing\t\tClimbing\tForaging')
    print('-' * 60)
    for i in info:
        print(f'{i[0]:^9}{i[1]:^22}{i[2]:>2}{i[3]:>12}{i[4]:>12}')

    c.close()
    conn.close()



def humanObservedBehavior():
    query = """
    SELECT 
        CASE 
            WHEN Approaches = 'true' OR Indifferent = 'true' OR `Runsfrom` = 'true' THEN 'Near Humans'
            ELSE 'Not Near Humans'
        END AS Human_Proximity,
        SUM(CASE WHEN Running = 'true' THEN 1 ELSE 0 END),
        SUM(CASE WHEN Chasing = 'true' THEN 1 ELSE 0 END),
        SUM(CASE WHEN Climbing = 'true' THEN 1 ELSE 0 END),
        SUM(CASE WHEN Eating = 'true' THEN 1 ELSE 0 END),
        SUM(CASE WHEN Foraging = 'true' THEN 1 ELSE 0 END),
        SUM(
            CASE
                WHEN TailFlags = 'true' THEN 1 ELSE 0 
            END +
            CASE 
                WHEN TailTwitches = 'true' THEN 1 ELSE 0 
            END
            ),
        SUM(
            CASE 
                WHEN Kuks = 'true' THEN 1 ELSE 0 
            END + 
            CASE 
                WHEN Quaas = 'true' THEN 1 ELSE 0 
            END + 
            CASE 
                WHEN Moans = 'true' THEN 1 ELSE 0 
            END
        )
    FROM squirreldata
    GROUP BY Human_Proximity
    ORDER BY Human_Proximity;
    """
    c.execute(query)
    info = c.fetchall()
    print(f'\nObserved Behavior of Squirrels near Humans:')
    print(f'\nHuman Proximity\t\tRunning\t\tChasing\t\tClimbing\tEating\t\tForaging\t\t'
          f'Tail Communication\t\tVocal Communication')
    print('-' * 127)

    print(f'{info[0][0]}{info[0][1]:>14}{info[0][2]:^22}{info[0][3]}'
          f'{info[0][4]:^18}{info[0][5]:^8}{info[0][6]:^35}{info[0][7]:^10}')
    print(f'{info[1][0]}{info[1][1]:^18}{info[1][2]:^6}{info[1][3]:>11}'
          f'{info[1][4]:^18}{info[1][5]:^10}{info[1][6]:>17}{info[1][7]:>22}')

    c.close()
    conn.close()



if __name__ == '__main__':
    runQuery()

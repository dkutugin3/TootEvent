1. /registration (post)
	регистрация нового пользователя
	- username: str
    - email: str
    - password: str

2. /login (post)
	аутентификация пользователя
	- username / email: str
	- password: str

3. /logout (post)

4. /users (get)
	получение информации о всех юзерах

5. /users/{user_id} (get)
	информация о конкретном юзере
6. /users/{user_id} (patch)
	изменение информации о юзере
7. /users/{user_id} (delete)
	удаление юзера

8. /events (get)
	получение информации о всех ивентах
9. /events (put)
	добавление нового ивента
	- title: str
	- price: int
	- genre: set (?)
	- location: location
	- date: date

10. /events/{event_id} (get)
	информация о конкретном ивенте
11. /events/{event_id} (patch)
	изменение информации об ивенте
12. /events/{event_id} (delete)
	удаление ивента

13. /bookings (get)
	получение информации о всех бронях
14. /bookings (put)
	создание брони
	- user_id: int
	- event_id: int
	- date: date

15. /bookings/{booking_id} (get)
	получение информации о конкретной брони
16. /bookings/{booking_id} (patch)
	изменение информации о брони
17. /bookings/{booking_id} (delete)
	удаление брони

18. /events/{filters} (get) ???
	получение ивентов по фильтрам
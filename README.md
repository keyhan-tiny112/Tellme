Tellme
=======
Tellme is mini messager server and client with FastAPI. (in python)

> ### ⚠️ warning ⚠️
> This is an experimental project for fun.
> Please do not use it in real environments!

Usege
======
> port: 8999
> host: 127.0.0.1

routes
-------
- `/SetName`
  > Set of name
  > ### schema
    > ```json
    > {
    >   "name": <string>
    > }
    > ```
- `/SendMsg`
  > Send of Your Message
  > ### schema
    > ```json
    > {
    >   "msg": <string>
    > }
    > ```
- `/GiveMsg`
  > Give of Massages
  > ### schema
    > ```json
    > {
    >   "sender": <string>
    >   "msg": <string>
    > }
    > ```

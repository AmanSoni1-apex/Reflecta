<!-- To implement the JWT we are installing two libraries and that are :-  -->

1. python-jose[cryptography] -> it handlies the passwoord hashing , when the user registers with the password we are hashing the password using this lib and storing it in something like `$2b$12$KIXxyz...` so that even if someone steals your database they can't get the original password.

2. passlib[bcrypt] -> it is used to handle the  JWT creation and verification , this is what creates the "header.payload.signature" token and verify it on every request.

<!-- HASHING ALGO'S -->
Their are the 2 families of the hashing algo's ->

1. Symmetric (HS256, HS384, HS512) — one secret key does both signing and verification. Same key creates the token and reads it. Simple, fast, perfect when your backend is one system talking to itself.

2. Asymmetric (RS256, ES256) — two keys. Private key signs the token. Public key verifies it. Used when multiple different servers need to verify tokens independently — like Google's auth system where thousands of services verify Google tokens.

We chose HS256 because:
Reflecta has one backend. The same server that creates tokens also verifies them. One key is all we need. The 256 in HS256 means 256-bit key strength. means your secret key is a sequence of 256 zeros and ones. ( possible combination = 2 to the power of 256 possible keys , That's roughly 10 followed by 77 zeros )
Why can't you brute force it?
Brute forcing means trying every possible key until you find the right one. so , Even if you had a computer that could try a billion billion combinations per second — and used every computer on earth — you'd still need more time than the universe has existed to try them all.
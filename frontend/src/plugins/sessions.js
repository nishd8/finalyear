import jwt from 'jwt-simple'

const secret= process.env.VUE_APP_SESSION_KEY

function createUserSession(user){
    console.log(secret)
    var token = jwt.encode(user,secret)
    var key = jwt.encode('user',secret)
    localStorage.setItem(key,token)
}
function getSessionUser(){
    var key = jwt.encode('user',secret)
    var user =localStorage.getItem(key)
    return jwt.decode(user,secret)
}
function logout(router){
    localStorage.clear()
    router.push({name:"Home"})
}

export {createUserSession,getSessionUser,logout}
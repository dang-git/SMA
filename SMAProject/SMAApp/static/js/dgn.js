var desc = JSON.parse(descriptives);
console.log(desc);

document.getElementById("postsCount").innerHTML = desc['tweets'].toLocaleString();
document.getElementById("usersCount").innerHTML = desc['users'].toLocaleString();
document.getElementById("audienceCount").innerHTML = desc['reach'].toLocaleString();
document.getElementById("engagementsCount").innerHTML = desc['engagements'].toLocaleString();

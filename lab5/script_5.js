let ACCESS_TOKEN_MY = null;
let users = [];
let friendsData = {};

if ('VKIDSDK' in window) {
    const VKID = window.VKIDSDK;

    VKID.Config.init({
        app: 53351443,
        redirectUrl: 'http://localhost',
        responseMode: VKID.ConfigResponseMode.Callback,
        source: VKID.ConfigSource.LOWCODE,
        scope: 'wall photos status friends groups',
    });

    const oneTap = new VKID.OneTap();

    oneTap.render({
        container: document.currentScript.parentElement,
        showAlternativeLogin: true
    })
        .on(VKID.WidgetEvents.ERROR, vkidOnError)
        .on(VKID.OneTapInternalEvents.LOGIN_SUCCESS, function (payload) {
            const code = payload.code;
            const deviceId = payload.device_id;

            VKID.Auth.exchangeCode(code, deviceId)
                .then(vkidOnSuccess)
                .catch(vkidOnError);
        });

    function vkidOnSuccess(data) {
        alert("Вход выполнен!");
        ACCESS_TOKEN_MY = data.access_token;
        showField();
    }

    function vkidOnError(error) {
        console.log('Ошибка:', error);
    }
}

function showField() {
    document.getElementById("form").style.display = "block";
}


/*
function get_friends() {
    let group_id = document.getElementById("group_id").value;
    let count1 = document.getElementById("count1").value;
    let count2 = document.getElementById("count2").value;
    
    users = [];
    friendsData = {};
    document.getElementById("usersList").innerHTML = "";
    
    if (!group_id || !count1 || !count2) {
        alert("Заполните все поля!");
        return;
    }

    // Получаем участников группы
    $.getJSON({
        url: `https://api.vk.com/method/groups.getMembers?group_id=${group_id}&count=${count1}&fields=first_name,last_name&access_token=${ACCESS_TOKEN_MY}&v=5.199`,
        jsonp: "callback",
        dataType: "jsonp"
    }).done(function (data) {
        if (data.response && data.response.items) {
            users = data.response.items;
            document.getElementById("resultsContainer").style.display = "block";
            displayUsers();
            
            // Получаем друзей для каждого пользователя
            users.forEach(user => {
                getFriendsForUser(user.id, count2);
            });
        } else {
            alert("Ошибка: " + (data.error ? data.error.error_msg : "неверные данные"));
        }
    }).fail(function (error) {
        alert("Ошибка при получении участников");
    });
}

function getFriendsForUser(userId, count) {
    $.getJSON({
        url: `https://api.vk.com/method/friends.get?user_id=${userId}&access_token=${ACCESS_TOKEN_MY}&v=5.199&fields=first_name,last_name&order=hints&count=${count}`,
        jsonp: "callback",
        dataType: "jsonp"
    }).done(function (friendsResponse) {
        if (friendsResponse.response && friendsResponse.response.items) {
            friendsData[userId] = friendsResponse.response.items;
            updateUserFriendsDisplay(userId);
        } else {
            friendsData[userId] = [];
            updateUserFriendsDisplay(userId);
        }
    }).fail(function () {
        friendsData[userId] = [];
        updateUserFriendsDisplay(userId);
    });
}

function displayUsers() {
    const usersList = document.getElementById("usersList");
    
    users.forEach(user => {
        const userCard = document.createElement("div");
        userCard.className = "user-card";
        userCard.id = `user-${user.id}`;
        
        userCard.innerHTML = `
            <strong>${user.first_name} ${user.last_name}</strong>
            <div class="friends-list" id="friends-${user.id}">
                <p>Загрузка друзей...</p>
            </div>
        `;
        
        usersList.appendChild(userCard);
    });
}

function updateUserFriendsDisplay(userId) {
    const friendsContainer = document.getElementById(`friends-${userId}`);
    if (!friendsContainer) return;
    
    const friends = friendsData[userId] || [];
    
    let friendsHTML = "<p>Друзья:</p>";
    if (friends.length > 0) {
        friends.forEach(friend => {
            friendsHTML += `
                <div class="friend-item">
                    ${friend.first_name} ${friend.last_name}
                </div>
            `;
        });
    } else {
        friendsHTML += "<p>Нет друзей или доступ ограничен</p>";
    }
    
    friendsContainer.innerHTML = friendsHTML;
}*/


async function get_friends() {
    let group_id = document.getElementById("group_id").value;
    let count1 = document.getElementById("count1").value;
    let count2 = document.getElementById("count2").value;
    
    users = [];
    friendsData = {};
    document.getElementById("usersList").innerHTML = "";
    
    if (!group_id || !count1 || !count2) {
        alert("Заполните все поля!");
        return;
    }

    try {
        // Получаем участников группы
        const membersResponse = await $.getJSON({
            url: `https://api.vk.com/method/groups.getMembers?group_id=${group_id}&count=${count1}&fields=first_name,last_name&access_token=${ACCESS_TOKEN_MY}&v=5.199`,
            jsonp: "callback",
            dataType: "jsonp"
        });

        if (membersResponse.response && membersResponse.response.items) {
            users = membersResponse.response.items;
            document.getElementById("resultsContainer").style.display = "block";
            displayUsers();
            
            // Получаем друзей для каждого пользователя параллельно
            await Promise.all(users.map(user => getFriendsForUser(user.id, count2)));
        } else {
            alert("Ошибка: " + (membersResponse.error ? membersResponse.error.error_msg : "неверные данные"));
        }
    } catch (error) {
        alert("Ошибка при получении участников");
    }
}

async function getFriendsForUser(userId, count) {
    try {
        const friendsResponse = await $.getJSON({
            url: `https://api.vk.com/method/friends.get?user_id=${userId}&access_token=${ACCESS_TOKEN_MY}&v=5.199&fields=first_name,last_name&order=hints&count=${count}`,
            jsonp: "callback",
            dataType: "jsonp"
        });

        if (friendsResponse.response && friendsResponse.response.items) {
            friendsData[userId] = friendsResponse.response.items;
        } else {
            friendsData[userId] = [];
        }
    } catch (error) {
        friendsData[userId] = [];
    } finally {
        updateUserFriendsDisplay(userId);
    }
}

function displayUsers() {
    const usersList = document.getElementById("usersList");
    
    users.forEach(user => {
        const userCard = document.createElement("div");
        userCard.className = "user-card";
        userCard.id = `user-${user.id}`;
        
        userCard.innerHTML = `
            <strong>${user.first_name} ${user.last_name}</strong>
            <div class="friends-list" id="friends-${user.id}">
                <p>Загрузка друзей...</p>
            </div>
        `;
        
        usersList.appendChild(userCard);
    });
}

function updateUserFriendsDisplay(userId) {
    const friendsContainer = document.getElementById(`friends-${userId}`);
    if (!friendsContainer) return;
    
    const friends = friendsData[userId] || [];
    
    let friendsHTML = "<p>Друзья:</p>";
    if (friends.length > 0) {
        friends.forEach(friend => {
            friendsHTML += `
                <div class="friend-item">
                    ${friend.first_name} ${friend.last_name}
                </div>
            `;
        });
    } else {
        friendsHTML += "<p>Нет друзей или доступ ограничен</p>";
    }
    
    friendsContainer.innerHTML = friendsHTML;
}
import {API} from "/static/js/inbuiltAPI.js"

const DAY_NOW = (new Date()).getDay();


/*
TODO: Should we still use Django template tags to prevent users stop
      seeing timetable card for students or it's better to replace it
      with API call to check whether request.user is student?
*/
if (document.getElementById("timetable-app") !== null) {
    const timetableApp = new Vue({
    el: "#timetable-app",
    delimiters: ["[[", "]]"],
    data: {
        days: ["понедельник", "вторник", "среду", "четверг", "пятницу", "субботу"],
        currentDay: undefined,
        timetable: undefined,
        selectedDay: ((DAY_NOW === 0) ? 1 : DAY_NOW),
    },
    methods: {
        getTimetable: function () {
            let vm = this;
            API.timetable.list("9", "З", (data) => {
                vm.timetable = data;
                vm.currentDay = data.find(value => value.weekday === vm.selectedDay);
            })
        },
        renderTime: function (s) {
            return s.slice(((s[0] === "0") ? 1 : 0), 5);
        },
        changeDay: function (mode) {
            if (mode === "prev") {
                if (this.selectedDay > 1) this.selectedDay--;
            } else {
                if (this.selectedDay < 6) this.selectedDay++;
            }
            if (this.timetable) this.currentDay = this.timetable.find(value => value.weekday === this.selectedDay);
        },
        getDayName: function (day) {
            let now = new Date();
            let distance = day - now.getDay();
            now.setDate(now.getDate() + distance);
            return now.toLocaleString("ru", {weekday: "short"}).toUpperCase();
        }
    }
})
    document.addEventListener("DOMContentLoaded", function() {
        timetableApp.getTimetable();
    })
}


// TODO: Finish working on news card.
const newsApp = new Vue({
    el: "#news-app",
    delimiters: ["[[", "]]"],
    data: {
        news: undefined
    },
    methods: {
        getNews: function () {

        }
    }
})

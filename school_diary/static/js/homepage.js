const timetableApp = new Vue({
    el: "#timetable-app",
    delimiters: ["[[", "]]"],
    data: {
        days: ["понедельник", "вторник", "среду", "четверг", "пятницу", "субботу"],
        currentDay: undefined,
        timetable: undefined,
        selectedDay: (new Date()).getDay()
    },
    methods: {
        getTimetable: function () {
            let vm = this;
            $.ajax("/api/timetable/9/%D0%97/", {
                /**
                 * @param {Array} data
                 */
                success: function (data) {
                    vm.timetable = data;
                    vm.currentDay = data.find(value => value.weekday === vm.selectedDay);
                },
                error: function (...args) {
                    vm.timetable = {};
                    vm.currentDay = [];
                }
            });
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


document.addEventListener("DOMContentLoaded", function() {
    timetableApp.getTimetable();
})



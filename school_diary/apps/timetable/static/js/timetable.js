import {API} from '/static/js/inbuiltAPI.js'


const timeTableApp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#timetable',
    data: {
        days: [],
        empty: false,
    },
    methods: {
        getDayName: function (day) {
            let now = new Date();
            let distance = day - now.getDay();
            now.setDate(now.getDate() + distance);
            let r = now.toLocaleString("ru", {weekday: "long"});
            r = r[0].toUpperCase() + r.slice(1);
            return r;
        },
        renderTime: function (s) {
            return s.slice(((s[0] === "0") ? 1 : 0), 5);
        },
        checkTimeTable: function (data) {
            let counter = 0;
            for (let i = 2; i < data.length; i++) {
                if (!data[i].lessons.length)
                    counter++;
            }
            if (counter === 0) return 0;
            if (counter === 7) return 1;
            return 2;
        },
        getTimeTable: function () {
            let vm = this;
            let number = $('#id_grade').val();
            let letter = $('#id_litera').val();
            API.timetable.list(number, letter, function(data) {
                switch (vm.checkTimeTable(data)) {
                    case 2:
                        vm.empty = false;
                        break;
                    case 1:
                        vm.empty = true;
                        break;
                    case 0:
                        vm.empty = false;
                        break;
                }
                vm.days = data;
            }, {
                error: function (e) {
                    vm.empty = true;
                }
            })
        }
    }
})

$(document).ready(function () {
    $("#timetable_btn").on("click", function () {
        timeTableApp.getTimeTable();
    });
});

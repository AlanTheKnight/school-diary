const csrf = Cookies.get("csrftoken");

const BASE_URL = "/api/";
const editLessonAPIURL = "inbuilt/lessons/";
const listLessonsAPIURL = "inbuilt/lessons/";
const listControlsAPIURL = 'inbuilt/controls/';
const getGradesTableAPIURL = 'inbuilt/grades/table/';
const getGradesAPIURL = 'inbuilt/grades/'
const getGroupAPIURL = 'inbuilt/grades/group';
const saveGradeAPIURL = 'inbuilt/save-mark';

const URLS = {
    homework: {
        list: 'inbuilt/homework/',
    },
    users: {
        list: 'inbuilt/users/',
        details: 'inbuilt/users/'
    },
    timetable: {
        list: 'timetable/',
        current: 'timetable/'
    }
}


/**
 * @callback ajaxCallCallback
 * @param {Object} data
 */

/**
 * @param {String} method
 * @param {String} url
 * @param {Object} data
 * @param {ajaxCallCallback} callback
 * @param {Object} options
 * @param {Array} filters
 */
function inbuiltAPIWrapper(
    method, url, data = null,
    callback = null, options = null, filters = null) {
    let ajax_url = BASE_URL + encodeURI(url);
    if (filters) {
        let params = [];
        for (let value of filters) {
          params.push(`${value[0]}=${value[1]}`);
        }
        ajax_url += "?" + params.join("&");
        console.log(ajax_url);
    }
    let parameters = {
        headers: {
            "X-CSRFToken": csrf,
        },
        data: data,
        url: ajax_url,
        method: method,
        success: function (data) {
            if (callback) callback(data);
        },
    }
    if (options) {
        for (let k in options) parameters[k] = options[k];
    }
    $.ajax(parameters);
}


export const API = {
    lessons: {
        /**
         * @param {Number} pk - primary key of a lesson
         * @param {Object} data
         * @param {ajaxCallCallback} callback
         * @param {Object} options
         */
        edit: function (pk, data, callback = null, options = null) {
            inbuiltAPIWrapper(
                "PATCH",
                editLessonAPIURL + pk,
                data, callback, options
            );
        },
        /**
         * @param {Number} pk - primary key of a lesson
         * @param {ajaxCallCallback} callback
         */
        get: function (pk, callback = null) {
            inbuiltAPIWrapper("GET", editLessonAPIURL + pk, null, callback);
        },
        /**
         * @param {Number} pk - primary key of a lesson
         * @param {ajaxCallCallback} callback
         */
        delete: function (pk, callback = null) {
            inbuiltAPIWrapper("DELETE", editLessonAPIURL + pk, null, callback);
        },
        list: function (data, callback = null) {
            inbuiltAPIWrapper("GET", listLessonsAPIURL, data, callback)
        }
    },
    controls: {
        /**
         * @param {ajaxCallCallback} callback
         */
        list: function (callback = null) {
            inbuiltAPIWrapper("GET", listControlsAPIURL, null, callback);
        }
    },
    /**
     *
     * @param {Number} group
     * @param {Number} quarter
     * @param {ajaxCallCallback} callback
     */
    getGradesTable: function (group, quarter, callback = null) {
        inbuiltAPIWrapper("POST", getGradesTableAPIURL, {
            group: group, quarter: quarter
        }, callback);
    },
    groups: {
        get: function (data, callback = null) {
            inbuiltAPIWrapper("POST", getGroupAPIURL, data, callback);
        }
    },
    grades: {
        get: function (data, callback = null) {
            inbuiltAPIWrapper("GET", getGradesAPIURL, data, callback)
        },
        save: function (data, callback = null) {
            inbuiltAPIWrapper("POST", saveGradeAPIURL, data, callback);
        }
    },
    comments: {
        get: function (student, lesson, callback = null) {
            inbuiltAPIWrapper("GET", getGradesAPIURL, {
                student: student, lesson: lesson
            }, callback)
        },
    },
    homework: {
        list: function (callback = null, filters = null) {
            inbuiltAPIWrapper("GET", URLS.homework.list, null, callback, null, filters)
        }
    },
    users: {
        list: function (callback = null, filters = null) {
            inbuiltAPIWrapper("GET", URLS.homework.list, null, callback, null, filters)
        }
    },
    timetable: {
        list: function (number, letter, callback = null, options = null) {
            let url = URLS.timetable.list + number + letter;
            inbuiltAPIWrapper("GET", url, null, callback, options);
        },
        current: function (callback = null, options = null) {
            inbuiltAPIWrapper("GET", URLS.timetable.current, null, callback, options);
        }
    }
}

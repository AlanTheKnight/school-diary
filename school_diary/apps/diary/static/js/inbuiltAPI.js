const csrf = Cookies.get("csrftoken");

const BASE_URL = "/api/inbuilt/";
const editLessonAPIURL = "lessons/";
const listLessonsAPIURL = "lessons/";
const listControlsAPIURL = 'controls/';
const getGradesTableAPIURL = 'grades/table/';
const getGradesAPIURL = 'grades/'
const getGroupAPIURL = 'grades/group';
const saveGradeAPIURL = 'save-mark';

const URLS = {
    homework: {
        list: 'homework/'
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
 * @param {Object} filters
 */
function inbuiltAPIWrapper(
    method, url, data = null,
    callback = null, options = null, filters = null) {
    let ajax_url = BASE_URL + url;
    if (filters) {
        let params = [];
        for (let [key, value] of Object.entries(filters)) {
          params.push(`${key}=${value}`);
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
    }
}

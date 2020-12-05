/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./www.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./app.js":
/*!****************!*\
  !*** ./app.js ***!
  \****************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/* WEBPACK VAR INJECTION */(function(__dirname) {var createError = __webpack_require__(/*! http-errors */ \"http-errors\");\r\nvar express = __webpack_require__(/*! express */ \"express\");\r\nvar path = __webpack_require__(/*! path */ \"path\");\r\nvar cookieParser = __webpack_require__(/*! cookie-parser */ \"cookie-parser\");\r\nvar logger = __webpack_require__(/*! morgan */ \"morgan\");\r\nvar mysql = __webpack_require__(/*! mysql */ \"mysql\");\r\n\r\n//var fileUploadRouter = require('./routes/upload');\r\n//var listRouter = require('./routes/list');\r\nvar mysqlConfig = __webpack_require__(/*! ./config/mysql.config */ \"./config/mysql.config.js\");\r\nvar downloadRouter = __webpack_require__(/*! ./routes/download */ \"./routes/download.js\");\r\n\r\nvar app = express();\r\n\r\n\r\n// view engine setup\r\napp.set('views', path.join(__dirname, 'views'));\r\napp.set('view engine', 'ejs');\r\n\r\napp.use(logger('dev'));\r\napp.use(express.json());\r\napp.use(express.urlencoded({ extended: false }));\r\napp.use(cookieParser());\r\napp.use(express.static(path.join(__dirname, 'public')));\r\n\r\n\r\nmysqlConfig.connection = mysql.createConnection(mysqlConfig.config);\r\n\r\napp.use('/', downloadRouter);\r\n//app.use('/upload', fileUploadRouter);\r\n//app.use('./upload', express.static('upload'));\r\n//app.use('/list', listRouter);\r\n//app.use('/download', downloadRouter);\r\n// catch 404 and forward to error handler\r\napp.use(function(req, res, next) {\r\n  next(createError(404));\r\n});\r\n\r\n// error handler\r\napp.use(function(err, req, res, next) {\r\n  // set locals, only providing error in development\r\n  res.locals.message = err.message;\r\n  res.locals.error = req.app.get('env') === 'development' ? err : {};\r\n\r\n  // render the error page\r\n  res.status(err.status || 500);\r\n  res.render('error');\r\n});\r\n\r\nmodule.exports = app;\r\n\n/* WEBPACK VAR INJECTION */}.call(this, \"/\"))\n\n//# sourceURL=webpack:///./app.js?");

/***/ }),

/***/ "./config/mysql.config.js":
/*!********************************!*\
  !*** ./config/mysql.config.js ***!
  \********************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("const mysqlConfig =  {\r\n    config: {\r\n      host: \"portalabdb.cj1xmu0ufgki.ap-northeast-2.rds.amazonaws.com\",\r\n      user: \"portalab\",\r\n      database: \"portalab\",\r\n      password: \"gogiparty\",\r\n      port: \"3306\"\r\n    },\r\n    connection: undefined\r\n  }\r\n  \r\n  module.exports = mysqlConfig;\n\n//# sourceURL=webpack:///./config/mysql.config.js?");

/***/ }),

/***/ "./routes/download.js":
/*!****************************!*\
  !*** ./routes/download.js ***!
  \****************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("var express = __webpack_require__(/*! express */ \"express\");\r\nvar router = express.Router();\r\nvar mysql = __webpack_require__(/*! mysql */ \"mysql\");\r\nvar mysqlConfig = __webpack_require__(/*! ../config/mysql.config */ \"./config/mysql.config.js\");\r\nvar ejs = __webpack_require__(/*! ejs */ \"ejs\");\r\nvar fs = __webpack_require__(/*! fs */ \"fs\");\r\nvar shelljs = __webpack_require__(/*! shelljs */ \"shelljs\");\r\nconst { resolve } = __webpack_require__(/*! path */ \"path\");\r\nconst { response } = __webpack_require__(/*! express */ \"express\");\r\n\r\nvar sql = 'SELECT file_id, file_name FROM stl_storage';\r\nvar rst;\r\nrouter.get('/', (req, res, next) => {\r\n    sql = 'SELECT file_id, file_name FROM stl_storage';\r\n    mysqlConfig.connection.query(sql, function(err, result) {\r\n        rst = result;\r\n        if(err) {\r\n            console.log(err);\r\n        }\r\n        var html = ``;\r\n        for(let i = 0; i < result.length; i++) {\r\n            html += `<p>${result[i].file_id}. ${result[i].file_name}</p>`\r\n        }\r\n        html += `<form action = '/' method = \"post\"> number: <select name = \"number\">`;\r\n        for(let i = 0; i < result.length; i++) {\r\n            html += `<option value = ${i}> ${i+1} </option>`\r\n        }\r\n        html += `</select> <input type = \"submit\" value = \"submit\"> </form>`\r\n        res.send(html);\r\n    });\r\n});\r\n\r\nrouter.post('/', async (req, res, next) => {\r\n    \r\n    var file_id = req.body.number;\r\n    var file_name = rst[file_id].file_name.replace(/ /g, \"\");\r\n    sql = `SELECT file FROM stl_storage WHERE file_id=${file_id}`;\r\n    await test(sql, file_name).then(() => { console.log(`writing`)});\r\n    console.log(`finish`);\r\n\r\n    setTimeout(() => {\r\n        let output_name = file_name.substr(0, file_name.length - 4);\r\n        shelljs.exec(`/home/junsang/cura/CuraEngine/build/CuraEngine slice -v -j /home/junsang/cura/Cura/resources/definitions/anet3d_a8.def.json -o /home/junsang/cura_node/gcode/${output_name}.gcode -l /home/junsang/cura_node/upload/${file_name}`);\r\n        res.download(`/home/junsang/cura_node/gcode/${output_name}.gcode`);\r\n    }, 50);\r\n    /*\r\n    let fd = fs.openSync('settings.sh', 'w');\r\n\r\n    fs.appendFileSync(fd, `! /bin/bash \\r\\ncd /home/user/cura/CuraEngine/\\n./build/CuraEngine slice -v -j /home/user/cura/Cura/resources/definitions/anet3d_a8.def.json -o /home/user/cura_node/gcode/${file_name}.gcode -l /home/user/cura_node/upload/${file_name}`);\r\n    \r\n    fs.closeSync(fd);\r\n\r\n    shelljs.exec('chmod 755 settings.sh');\r\n    shelljs.exec('sudo ./settings.sh');*/\r\n    //shelljs.exec();\r\n    //shelljs.exec(`/home/user/cura/CuraEngine/build/CuraEngine slice -v -j /home/user/cura/Cura/resources/definitions/anet3d_a8.def.json -o /home/user/cura_node/gcode/${file_name}.gcode -l /home/user/cura_node/upload/${file_name}`);\r\n\r\n    //res.sendFile(`/home/user/cura_node/gcode/${file_name}.gcode`);\r\n});\r\n\r\n\r\nasync function test(sql, file_name) {\r\n    mysqlConfig.connection.query(sql, function(err, result) {\r\n        if(err) {\r\n            console.log(err);\r\n        }\r\n        else{\r\n            try {\r\n                let buf = b(result).then((data) => {\r\n                    fs.writeFileSync(`./upload/${file_name}`, data);\r\n                }).catch((err) => { console.log(`err on function try`); });\r\n                return `finish`;\r\n            } catch(err) {\r\n                console.log(`err on function catch`);\r\n                return err;\r\n            }\r\n        }\r\n    });\r\n};\r\n\r\nasync function b(result) {\r\n    let buf = new Buffer(result[0].file, \"binary\");\r\n    try{\r\n        return await buf;\r\n    } catch(err) {\r\n        console.log(`err on function b`);\r\n        return err;\r\n    }\r\n};\r\n\r\nmodule.exports = router;\n\n//# sourceURL=webpack:///./routes/download.js?");

/***/ }),

/***/ "./www.js":
/*!****************!*\
  !*** ./www.js ***!
  \****************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/**\n * Module dependencies.\n */\n\nvar app = __webpack_require__(/*! ./app */ \"./app.js\");\nvar debug = __webpack_require__(/*! debug */ \"debug\")('cura-node:server');\nvar http = __webpack_require__(/*! http */ \"http\");\n\n/**\n * Get port from environment and store in Express.\n */\n\nvar port = normalizePort(process.env.PORT || '80');\napp.set('port', port);\n\n/**\n * Create HTTP server.\n */\n\nvar server = http.createServer(app);\n\n/**\n * Listen on provided port, on all network interfaces.\n */\n\nserver.listen(port);\nserver.on('error', onError);\nserver.on('listening', onListening);\n\n/**\n * Normalize a port into a number, string, or false.\n */\n\nfunction normalizePort(val) {\n  var port = parseInt(val, 10);\n\n  if (isNaN(port)) {\n    // named pipe\n    return val;\n  }\n\n  if (port >= 0) {\n    // port number\n    return port;\n  }\n\n  return false;\n}\n\n/**\n * Event listener for HTTP server \"error\" event.\n */\n\nfunction onError(error) {\n  if (error.syscall !== 'listen') {\n    throw error;\n  }\n\n  var bind = typeof port === 'string'\n    ? 'Pipe ' + port\n    : 'Port ' + port;\n\n  // handle specific listen errors with friendly messages\n  switch (error.code) {\n    case 'EACCES':\n      console.error(bind + ' requires elevated privileges');\n      process.exit(1);\n      break;\n    case 'EADDRINUSE':\n      console.error(bind + ' is already in use');\n      process.exit(1);\n      break;\n    default:\n      throw error;\n  }\n}\n\n/**\n * Event listener for HTTP server \"listening\" event.\n */\n\nfunction onListening() {\n  var addr = server.address();\n  var bind = typeof addr === 'string'\n    ? 'pipe ' + addr\n    : 'port ' + addr.port;\n  debug('Listening on ' + bind);\n}\n\n\n//# sourceURL=webpack:///./www.js?");

/***/ }),

/***/ "cookie-parser":
/*!********************************!*\
  !*** external "cookie-parser" ***!
  \********************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = require(\"cookie-parser\");\n\n//# sourceURL=webpack:///external_%22cookie-parser%22?");

/***/ }),

/***/ "debug":
/*!************************!*\
  !*** external "debug" ***!
  \************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = require(\"debug\");\n\n//# sourceURL=webpack:///external_%22debug%22?");

/***/ }),

/***/ "ejs":
/*!**********************!*\
  !*** external "ejs" ***!
  \**********************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = require(\"ejs\");\n\n//# sourceURL=webpack:///external_%22ejs%22?");

/***/ }),

/***/ "express":
/*!**************************!*\
  !*** external "express" ***!
  \**************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = require(\"express\");\n\n//# sourceURL=webpack:///external_%22express%22?");

/***/ }),

/***/ "fs":
/*!*********************!*\
  !*** external "fs" ***!
  \*********************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = require(\"fs\");\n\n//# sourceURL=webpack:///external_%22fs%22?");

/***/ }),

/***/ "http":
/*!***********************!*\
  !*** external "http" ***!
  \***********************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = require(\"http\");\n\n//# sourceURL=webpack:///external_%22http%22?");

/***/ }),

/***/ "http-errors":
/*!******************************!*\
  !*** external "http-errors" ***!
  \******************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = require(\"http-errors\");\n\n//# sourceURL=webpack:///external_%22http-errors%22?");

/***/ }),

/***/ "morgan":
/*!*************************!*\
  !*** external "morgan" ***!
  \*************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = require(\"morgan\");\n\n//# sourceURL=webpack:///external_%22morgan%22?");

/***/ }),

/***/ "mysql":
/*!************************!*\
  !*** external "mysql" ***!
  \************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = require(\"mysql\");\n\n//# sourceURL=webpack:///external_%22mysql%22?");

/***/ }),

/***/ "path":
/*!***********************!*\
  !*** external "path" ***!
  \***********************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = require(\"path\");\n\n//# sourceURL=webpack:///external_%22path%22?");

/***/ }),

/***/ "shelljs":
/*!**************************!*\
  !*** external "shelljs" ***!
  \**************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = require(\"shelljs\");\n\n//# sourceURL=webpack:///external_%22shelljs%22?");

/***/ })

/******/ });
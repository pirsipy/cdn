local size = ngx.var.size
local blur = ngx.var.blur
local source_file = ngx.var.source_file
local cache_path = ngx.var.cache_path
local cache_file = ngx.var.cache_file

local function return_error(status, msg)
    ngx.status = status
    ngx.header["Content-type"] = "text/html"
    ngx.say(msg)
    ngx.exit(0)
end

local file = io.open(source_file)
if not file then
    return_error(ngx.HTTP_NOT_FOUND, "Not found.")
end
file:close()

if string.find(size, "x") == nil then
    return_error(ngx.HTTP_BAD_REQUEST, "Invalid size format.")
end

if not (blur == "") then
    blur = tonumber(blur)
    if blur > 100 then
        return_error(ngx.HTTP_BAD_REQUEST, "Invalid blur.")
    end
end

if io.open(cache_path, "r") == nil then
    os.execute("mkdir -p " .. cache_path)
end

package.path = package.path .. ";" .. ngx.var.magick_path
local magick = require("magick")
magick.thumb(source_file, size:gsub("c", "#"), cache_file)

if not (blur == "") then
    img = magick.load_image(cache_file)
    img:blur(blur)
    img:write(cache_file)
    img:destroy()
end

ngx.exec(ngx.var.request_uri)

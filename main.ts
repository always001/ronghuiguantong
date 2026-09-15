// main.ts — Deno Deploy 静态文件服务器
import { serveDir } from "https://deno.land/std/http/file_server.ts";

Deno.serve((req) => {
  return serveDir(req, {
    fsRoot: ".",          // 从仓库根目录读取所有文件
    urlRoot: "",          // 根路径就是网站根
    showDirListing: false,// 禁止目录列表
    enableCors: true      // 允许跨域（前端 SPA 更稳）
  });
});

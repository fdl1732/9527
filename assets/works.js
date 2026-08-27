// ================================================================
// 📁 作品数据 — 在这里添加新作品
// 添加方式：在 works 数组末尾加一个新对象即可
// ================================================================

const works = [
  {
    id: "blackhole",
    title: "移动黑洞吞噬 · 大粒+快粒",
    desc: "鼠标控制黑洞移动，吞噬周围的粒子。包含大质量粒子（橙红）和高速光子（青蓝）两种类型。",
    tags: ["visual", "interactive", "html"],
    date: "2026-05-30",
    href: "works/blackhole.html"
  },
  {
    id: "human-model",
    title: "人体模型",
    desc: "交互式 3D 人体模型展示",
    tags: ["visual", "interactive", "html"],
    date: "2026-05-30",
    href: "works/body-model.html"
  },
  {
    id: "tornado-particles",
    title: "龙卷风粒子",
    desc: "模拟龙卷风中粒子的运动轨迹",
    tags: ["visual", "interactive", "html"],
    date: "2026-05-31",
    href: "works/tornado-particles.html"
  },
  {
    id: "water-vortex",
    title: "水旋涡 · 粒子投放",
    desc: "半透明水旋涡特效，点击投放黄色粒子，被旋涡吸入顶端后螺旋下坠消散。",
    tags: ["visual", "interactive", "html"],
    date: "2026-06-07",
    href: "works/water-vortex.html"
  },
  {
    id: "tower-defense",
    title: "方块世界塔防",
    desc: "Minecraft风格3D塔防游戏。建造箭塔抵御僵尸入侵，击杀获取资源，支持触屏和键鼠操作。",
    tags: ["visual", "interactive", "html"],
    date: "2026-08-23",
    href: "works/tower-defense.html"
  },
  {
    id: "mc-pvp",
    title: "方块对战 · 红蓝射击",
    desc: "Minecraft风格第一人称红蓝对战射击。可破坏树木/墙体并自动恢复，不同电脑联网对打，支持平板触屏与电脑键鼠。",
    tags: ["visual", "interactive", "html"],
    date: "2026-08-24",
    href: "works/mc-pvp.html"
  },
  {
    id: "survival",
    title: "生存挑战 · 联机塔防",
    desc: "Minecraft风格3D生存游戏。建造围墙和箭塔抵御僵尸入侵，击杀获取资源，支持联机协作。",
    tags: ["visual", "interactive", "html"],
    date: "2026-08-27",
    href: "works/survival.html"
  },
  {
    id: "shooting",
    title: "联机射击闯关",
    desc: "Minecraft风格多人联机射击游戏。WASD移动，左键开枪，和好友一起对抗越来越多的僵尸波次。",
    tags: ["visual", "interactive", "html"],
    date: "2026-08-27",
    href: "works/联机射击闯关.html"
  },

  // ─────────────────────────────────────────────────────────────
  // 📌 添加新作品示例（复制下面取消注释即可）：
  //
  // {
  //   id: "my-work",
  //   title: "作品标题",
  //   desc: "作品简要描述",
  //   tags: ["visual", "html"],   // 可选标签: html, visual, interactive, novel, document
  //   date: "2026-06-01",
  //   href: "works/my-work.html"   // 文件路径
  // }
  // ─────────────────────────────────────────────────────────────
];

// ================================================================
// 渲染逻辑 — 不需要修改
// ================================================================

const TAG_LABELS = {
  html: "HTML",
  visual: "视觉",
  interactive: "交互",
  novel: "小说",
  document: "文档"
};

function renderGallery() {
  const container = document.getElementById("gallery");
  if (!container) return;

  container.innerHTML = works.map(w => {
    const tagsHtml = w.tags.map(t =>
      `<span class="tag ${t}">${TAG_LABELS[t] || t}</span>`
    ).join("");

    // 对于 HTML 页面作品，在卡片中嵌入 iframe 预览
    const isHtml = w.tags.includes("html");
    const thumb = isHtml
      ? `<iframe src="${w.href}" loading="lazy"></iframe>`
      : `<span>📄</span>`;

    return `
      <a class="card" href="${w.href}" target="_blank">
        <div class="card-thumb">${thumb}</div>
        <div class="card-body">
          <div class="card-title">${w.title}</div>
          <div class="card-desc">${w.desc}</div>
          <div class="card-tags">${tagsHtml}</div>
          <div class="card-date">${w.date}</div>
        </div>
      </a>
    `;
  }).join("");
}

document.addEventListener("DOMContentLoaded", renderGallery);

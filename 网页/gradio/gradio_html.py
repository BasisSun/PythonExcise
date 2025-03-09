import gradio as gr

# 自定义CSS样式（保持原有设计）
custom_css = """
nav { justify-content: space-between; padding: 20px 50px; background: #f8f9fa; }
.logo { font-weight: bold; }
.nav-links a { margin-left: 30px; text-decoration: none; color: #333; }
/* 其他原有CSS样式... */
"""

# 创建Gradio界面
with gr.Blocks(css=custom_css) as demo:
    # 导航栏
    gr.HTML("""
    <nav>
        <div class="logo">AI古籍助理</div>
        <div class="nav-links">
            <a href="#">首页</a>
            <a href="#">登录</a>
        </div>
    </nav>
    """)

    # 主内容区域
    with gr.Column(scale=1, elem_classes="container"):
        # 标题区域
        gr.HTML("""
        <div class="features">
            <h1>古籍智能处理平台</h1>
            <p>一键提取古籍中的文字内容 · 自动标点 · 白话文翻译</p>
        </div>
        """)

        # 按钮组
        with gr.Row(elem_classes="button-group"):
            invite_btn = gr.Button("邀请好友一起用", elem_classes="btn")
            pdf_upload = gr.UploadButton("上传PDF文件", elem_classes="btn", file_types=[".pdf"])
            docx_upload = gr.UploadButton("上传DOCX文档", elem_classes="btn", file_types=[".docx"])

        # 拖拽上传区域
        with gr.Column(elem_classes="upload-area"):
            gr.HTML("""
            <div>点击或拖拽图片到此处上传</div>
            <div class="upload-tips">
                <div>支持批量上传图片</div>
                <div>支持直接粘贴截图 (Ctrl+V)</div>
            </div>
            """)
            image_upload = gr.File(file_count="multiple", file_types=["image"], visible=False)

        # 隐藏的组件用于处理逻辑
        output = gr.Textbox(visible=False)
        dummy = gr.Textbox(visible=False)

    # 事件处理函数
    def handle_pdf(files):
        return f"已接收PDF文件：{', '.join(f.name for f in files)}"

    def handle_docx(files):
        return f"已接收DOCX文件：{', '.join(f.name for f in files)}"

    def handle_images(files):
        return f"已接收图片文件：{', '.join(f.name for f in files)}"

    # 绑定事件
    pdf_upload.upload(
        handle_pdf,
        inputs=pdf_upload,
        outputs=output
    )

    docx_upload.upload(
        handle_docx,
        inputs=docx_upload,
        outputs=output
    )

    image_upload.upload(
        handle_images,
        inputs=image_upload,
        outputs=output
    )

    # 点击事件示例
    invite_btn.click(
        lambda: "邀请功能待实现",
        inputs=None,
        outputs=output
    )

    # 触发隐藏的文件选择器
    image_upload.select(
        lambda e: image_upload,
        inputs=None,
        outputs=image_upload
    )

# 启动应用
if __name__ == "__main__":
    demo.launch()
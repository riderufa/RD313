class Tag:
    def __init__(self, tag, klass=None, is_single=False, text='', **kwargs):
        self.tag = tag
        self.text = text
        self.attributes = {}
        self.is_single = is_single

        if klass:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
        if self.is_single:
            return ("<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs))
        else:
            return (
                "<{tag} {attrs}>\n{text}\n</{tag}>".format(
                    tag=self.tag, attrs=attrs, text=self.text
                )
            )

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
        if self.is_single:
            return ("<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs))
        else:
            return (
                "<{tag} {attrs}>\n{text}\n</{tag}>".format(
                    tag=self.tag, attrs=attrs, text=self.text
                )
            )


class TopLevelTag:  # для тегов
    def __init__(self, tag):
        self.tag = tag
        self.children = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        print("<%s>" % self.tag)
        for child in self.children:
            print(child)
        print("</%s>" % self.tag)

    def __str__(self):
        if self.children:
            opening = "<{tag}>".format(tag=self.tag)
            internal = ''
            for child in self.children:
                internal += str(child)
            ending = "</%s>" % self.tag
            return opening + internal + ending
        else:
            return "<{tag}></{tag}>".format(
                tag=self.tag
            )


if __name__ == "__main__":
    # with TopLevelTag("div", klass=("container", "container-fluid"), id="lead") as div:
    with TopLevelTag("body") as body:
        with TopLevelTag("div") as div:
            with Tag("img", is_single=True, src="/icon.png") as img:
                div.children.append(img)
            body.children.append(div)
#     with HTML(output=None) as doc:
#         with TopLevelTag("head") as head:
#             with Tag("title") as title:
#                 title.text = "hello"
#                 head += title
#             doc += head
#
#         with TopLevelTag("body") as body:
#             with Tag("h1", klass=("main-text",)) as h1:
#                 h1.text = "Test"
#                 body += h1
#
#             with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
#                 with Tag("p") as paragraph:
#                     paragraph.text = "another test"
#                     div += paragraph
#
#                 with Tag("img", is_single=True, src="/icon.png") as img:
#                     div += img
#
#                 body += div
#
#             doc += body

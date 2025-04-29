import {type RouteConfig, route, layout, index, prefix} from "@react-router/dev/routes";

export default [
    layout("./routes/root_layout.tsx", [
        // public routes
        index("./routes/home.tsx"),
        route("contact", "./routes/contact.tsx"),

        ...prefix("users", [
            route("auth", "./routes/users/auth.tsx"),
            route(":id", "./routes/users/user.tsx"),
        ]),

        ...prefix("books", [
            index("./routes/books/index.tsx"),
            route(":id", "./routes/books/book.tsx"),
            route("search", "./routes/books/search.tsx"),
        ]),

        // protected routes
        layout("./routes/protected_route.tsx", [
            ...prefix("users", [
                route("me", "./routes/users/me.tsx"),
            ])
        ])
    ]),
] satisfies RouteConfig;
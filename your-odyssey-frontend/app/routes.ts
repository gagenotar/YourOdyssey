import { type RouteConfig } from "@react-router/dev/routes";

export default [
  {
    file: "routes/_index.tsx",
    index: true
  },
  {
    path: "plan",
    file: "routes/plan.tsx"
  },
  {
    path: "my-trips",
    file: "routes/my-trips.tsx"
  },
  {
    path: "follows",
    file: "routes/follows.tsx"
  },
  {
    path: "follows/:id",
    file: "routes/followed-profile.tsx"
  },
  {
    path: "profile",
    file: "routes/profile.tsx"
  },
  {
    path: "login",
    file: "routes/login.tsx"
  },
  {
    path: "callback",
    file: "routes/callback.tsx"
  }
] satisfies RouteConfig;

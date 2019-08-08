let services = [
  {
    icon: "verified_user",
    name: "Django",
    href: "http://localhost/admin",
    type: "a",
    target: "_blank"
  },
  {
    icon: "local_florist",
    name: "Flower",
    href: "http://localhost/flower",
    type: "a",
    target: "_blank"
  },
  {
    icon: "email",
    name: "Mailhog",
    href: "http://localhost:8025",
    type: "a",
    target: "_blank"
  },
  {
    icon: "code",
    name: "GitLab",
    href: "https://gitlab.com/verbose-equals-true",
    type: "a",
    target: "_blank"
  }
];

if (process.env.NODE_ENV === "development") {
  services = [ ...services,
    {
      icon: "storage",
      name: "Redis Commander",
      href: "http://localhost:8081",
      type: "a",
      target: "_blank"
    }
  ];
}
console.log(JSON.stringify(services));
export default services;

export default defineEventHandler(async (event) => {
  return [
    {
      id: 1,
      title: "Workers' Compensation Act (NT)",
      category: "Compensation",
      jurisdiction: "NT",
      url: "https://wscc.nt.ca/about-wscc/policy-and-legislation/legislation"
    },
    {
      id: 2,
      title: "Safety Regulations (NU)",
      category: "Safety",
      jurisdiction: "NU",
      url: "https://wscc.nt.ca/about-wscc/policy-and-legislation/legislation"
    },
    {
      id: 3,
      title: "Mine Health & Safety Act",
      category: "Mining",
      jurisdiction: "NT/NU",
      url: "https://wscc.nt.ca/about-wscc/policy-and-legislation/legislation"
    }
  ]
})

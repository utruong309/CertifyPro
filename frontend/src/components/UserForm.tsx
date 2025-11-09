import { useState } from "react";
import API from "../api";
import { User } from "../types";

export default function UserForm() {
  const [user, setUser] = useState<User>({
    name: "",
    email: "",
    role: "",
    department: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) =>
    setUser({ ...user, [e.target.name]: e.target.value });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await API.post("/users/", user);
      alert("User created successfully!");
      setUser({ name: "", email: "", role: "", department: "" });
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    } catch (err) {
      alert("Error creating user");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form-box">
      <h3>Add User</h3>
      <input name="name" placeholder="Name" value={user.name} onChange={handleChange} required />
      <input name="email" placeholder="Email" value={user.email} onChange={handleChange} required />
      <input name="role" placeholder="Role" value={user.role} onChange={handleChange} required />
      <input
        name="department"
        placeholder="Department"
        value={user.department}
        onChange={handleChange}
      />
      <button type="submit">Create User</button>
    </form>
  );
}
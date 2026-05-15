import { createServerSupabaseClient } from "@/lib/supabase-server";
import { LoginForm } from "./components/login-form";
import { redirect } from "next/navigation";

export default async function Page() {
  const supabase = await createServerSupabaseClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (user) redirect("/");

  return (
    <div className="flex  min-h-0 w-full items-center justify-center p-6 md:p-10 ">
      <div className="w-full max-w-sm">
        <LoginForm />
      </div>
    </div>
  );
}

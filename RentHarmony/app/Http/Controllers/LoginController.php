<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Login;

class LoginController extends Controller
{
    public function adminlogin()
    {
        return view('Guest.adminlogin');
    }

    public function adminlogin_process(Request $request)
    {
        $username=$request->post("username");
        $password=$request->post("password");
        $checklogin=Login::where(["username"=>$username,"password"=>$password])->get();
        if(count($checklogin)==1)
        {
            $request->session()->put("username",$username);
            $request->session()->put("loginid",$checklogin[0]["loginid"]);
            return redirect()->route('index');
        }
        
    }
}
<?php

namespace App\Http\Controllers;

use App\Models\Service;
use Illuminate\Http\Request;

class HomeController extends Controller
{
    public function index()
    {
        $services = Service::orderBy('sort_order')->get();

        return view('welcome', compact('services'));
    }
}

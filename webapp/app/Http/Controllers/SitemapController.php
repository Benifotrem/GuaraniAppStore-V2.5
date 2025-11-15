<?php

namespace App\Http\Controllers;

use App\Models\Service;
use Illuminate\Http\Request;

class SitemapController extends Controller
{
    public function index()
    {
        $services = Service::where('status', 'active')->get();

        return response()->view('sitemap', compact('services'))
            ->header('Content-Type', 'application/xml');
    }
}

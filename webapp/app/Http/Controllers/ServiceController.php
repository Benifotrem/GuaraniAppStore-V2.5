<?php

namespace App\Http\Controllers;

use App\Models\Service;
use Illuminate\Http\Request;

class ServiceController extends Controller
{
    /**
     * Display service details
     */
    public function show($slug)
    {
        $service = Service::where('slug', $slug)->firstOrFail();

        // Calculate crypto price with discount
        $cryptoPrice = $service->price * (1 - (config('app.crypto_discount_percent', 25) / 100));

        return view('services.show', compact('service', 'cryptoPrice'));
    }
}

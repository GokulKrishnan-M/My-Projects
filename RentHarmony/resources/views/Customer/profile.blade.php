@extends('layouts.customermaster')
@section('content')
<style>
    body {
        background: #eef2f7;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .profile-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
    }
    .profile-card {
        background: #fff;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        max-width: 600px;
        width: 100%;
        transition: 0.3s;
    }
    .profile-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.12);
    }
    .profile-header {
        background: linear-gradient(135deg, #20247b, #93898aff);
        padding: 40px 20px;
        text-align: center;
        color: #fff;
    }
    .profile-header img {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 5px solid #fff;
        object-fit: cover;
        margin-bottom: 15px;
    }
    .profile-header h2 {
        font-size: 26px;
        margin: 10px 0 5px;
        font-weight: 700;
    }
    .profile-header h5 {
        font-size: 16px;
        font-weight: 400;
        opacity: 0.9;
    }
    .profile-body {
        padding: 30px;
    }
    .info-grid {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    .info-item {
        background: #f6f8fb;
        padding: 14px 18px;
        border-radius: 12px;
        font-size: 14px;
        color: #333;
        display: flex;
        justify-content: space-between; /* label left, value right */
        align-items: center;
    }
    .info-label {
        font-weight: bold;
        color: #20247b;
        flex: 1;
        text-align: left;
    }
    .info-value {
        flex: 2;
        text-align: center;
        color: #555;
    }
    .logout-container {
        display: flex;
        justify-content: center; /* Center horizontally */
        margin-top: 25px;
    }
    .logout-btn {
        padding: 10px 24px;
        background: #fc5356;
        color: #fff;
        border: none;
        border-radius: 8px;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        transition: 0.3s;
        text-decoration: none;
        text-align: center;
    }
    .logout-btn:hover {
        background: #e14b4e;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
</style>

<div class="profile-container">
    <div class="profile-card">
        <!-- Header -->
        <div class="profile-header">
            <img src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="Profile Avatar">
            <h2>{{ $customer->custname }}</h2>
            <h5>USERNAME: {{ $customer->username }}</h5>
        </div>

        <!-- Body -->
        <div class="profile-body">
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">EMAIL:</div>
                    <div class="info-value">{{ $customer->email }}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">PHONE NO:</div>
                    <div class="info-value">{{ $customer->contno }}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">REGISTERED DATE:</div>
                    <div class="info-value">{{ $customer->regdate }}</div>
                </div>
            </div>

            <!-- Logout Button -->
            <div class="logout-container">
                <form action="" method="POST">
                    @csrf
                    <button type="submit" class="logout-btn">Logout</button>
                </form>
            </div>
        </div>
    </div>
</div>
<br><br>
@endsection

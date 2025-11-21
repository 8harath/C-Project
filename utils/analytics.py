"""
Analytics utility functions for predictive insights and forecasting
"""
from datetime import datetime, timedelta
from collections import defaultdict
from models import db
from models.sale import Sale
from models.medicine import Medicine
from sqlalchemy import func


def calculate_moving_average(sales_data, window_size=3):
    """
    Calculate moving average for sales prediction

    Args:
        sales_data: List of tuples (date, value)
        window_size: Number of periods to average (default: 3)

    Returns:
        List of tuples (date, moving_average)
    """
    if len(sales_data) < window_size:
        return sales_data

    moving_averages = []

    for i in range(len(sales_data)):
        if i < window_size - 1:
            # Not enough data points yet
            moving_averages.append((sales_data[i][0], sales_data[i][1]))
        else:
            # Calculate average of last window_size values
            window = [sales_data[j][1] for j in range(i - window_size + 1, i + 1)]
            avg = sum(window) / window_size
            moving_averages.append((sales_data[i][0], avg))

    return moving_averages


def predict_next_period(sales_data, window_size=3):
    """
    Predict next period sales using moving average

    Args:
        sales_data: List of tuples (date, value)
        window_size: Number of periods to average

    Returns:
        Predicted value for next period
    """
    if len(sales_data) < window_size:
        if len(sales_data) > 0:
            return sum(val for _, val in sales_data) / len(sales_data)
        return 0

    # Use last window_size values
    recent_values = [val for _, val in sales_data[-window_size:]]
    return sum(recent_values) / len(recent_values)


def get_seasonal_trends():
    """
    Calculate seasonal sales trends

    Returns:
        Dictionary with seasonal data and predictions
    """
    # Get all sales
    sales = Sale.query.all()

    # Group by season
    seasonal_sales = defaultdict(float)
    seasonal_quantity = defaultdict(int)
    seasonal_count = defaultdict(int)

    for sale in sales:
        season = sale.get_season()
        seasonal_sales[season] += float(sale.total_price)
        seasonal_quantity[season] += sale.quantity_sold
        seasonal_count[season] += 1

    # Calculate current season
    current_month = datetime.now().month
    current_season = Sale.get_season_for_month(current_month)

    # Calculate averages
    seasonal_avg = {}
    for season in ['Winter', 'Spring', 'Summer', 'Monsoon']:
        if seasonal_count[season] > 0:
            seasonal_avg[season] = {
                'total_sales': seasonal_sales[season],
                'avg_per_transaction': seasonal_sales[season] / seasonal_count[season],
                'total_quantity': seasonal_quantity[season],
                'transaction_count': seasonal_count[season]
            }
        else:
            seasonal_avg[season] = {
                'total_sales': 0,
                'avg_per_transaction': 0,
                'total_quantity': 0,
                'transaction_count': 0
            }

    return {
        'seasonal_data': seasonal_avg,
        'current_season': current_season,
        'highest_season': max(seasonal_sales.items(), key=lambda x: x[1])[0] if seasonal_sales else None,
        'lowest_season': min(seasonal_sales.items(), key=lambda x: x[1])[0] if seasonal_sales else None
    }


def get_category_trends():
    """
    Get sales trends by category

    Returns:
        Dictionary with category sales data
    """
    # Query category-wise sales
    category_data = db.session.query(
        Medicine.category,
        func.sum(Sale.total_price).label('total_sales'),
        func.sum(Sale.quantity_sold).label('total_quantity'),
        func.count(Sale.sale_id).label('transaction_count')
    ).join(Sale).group_by(Medicine.category).all()

    category_trends = {}
    for category, total_sales, total_quantity, count in category_data:
        category_trends[category] = {
            'total_sales': float(total_sales),
            'total_quantity': int(total_quantity),
            'transaction_count': int(count),
            'avg_per_transaction': float(total_sales) / count if count > 0 else 0
        }

    return category_trends


def get_monthly_sales_data(months=12):
    """
    Get monthly sales data for the last N months

    Args:
        months: Number of months to retrieve (default: 12)

    Returns:
        List of tuples (month_label, total_sales)
    """
    start_date = datetime.now() - timedelta(days=months * 30)

    monthly_data = db.session.query(
        func.strftime('%Y-%m', Sale.sale_date).label('month'),
        func.sum(Sale.total_price).label('total_sales')
    ).filter(
        Sale.sale_date >= start_date
    ).group_by('month').order_by('month').all()

    return [(month, float(total_sales)) for month, total_sales in monthly_data]


def get_top_medicines_by_revenue(limit=10):
    """
    Get top medicines by revenue

    Args:
        limit: Number of medicines to return

    Returns:
        List of tuples (medicine_name, total_revenue, total_quantity)
    """
    top_medicines = db.session.query(
        Medicine.name,
        func.sum(Sale.total_price).label('revenue'),
        func.sum(Sale.quantity_sold).label('quantity')
    ).join(Sale).group_by(
        Medicine.medicine_id
    ).order_by(
        func.sum(Sale.total_price).desc()
    ).limit(limit).all()

    return [(name, float(revenue), int(quantity)) for name, revenue, quantity in top_medicines]


def get_stock_predictions():
    """
    Predict which medicines will run out of stock soon

    Returns:
        List of medicines with predicted stockout dates
    """
    predictions = []

    # Get medicines with sales history
    medicines_with_sales = db.session.query(
        Medicine.medicine_id
    ).join(Sale).distinct().all()

    medicine_ids = [m[0] for m in medicines_with_sales]

    for medicine_id in medicine_ids:
        medicine = Medicine.query.get(medicine_id)
        if not medicine or medicine.stock <= 0:
            continue

        # Get sales in last 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_sales = db.session.query(
            func.sum(Sale.quantity_sold)
        ).filter(
            Sale.medicine_id == medicine_id,
            Sale.sale_date >= thirty_days_ago
        ).scalar()

        if recent_sales and recent_sales > 0:
            # Calculate daily average
            daily_avg = recent_sales / 30.0

            # Predict days until stockout
            if daily_avg > 0:
                days_until_stockout = medicine.stock / daily_avg

                if days_until_stockout <= 30:  # Alert if less than 30 days
                    predicted_date = datetime.now() + timedelta(days=days_until_stockout)
                    predictions.append({
                        'medicine': medicine,
                        'current_stock': medicine.stock,
                        'daily_avg_sales': round(daily_avg, 2),
                        'days_until_stockout': int(days_until_stockout),
                        'predicted_stockout_date': predicted_date.date(),
                        'urgency': 'high' if days_until_stockout <= 7 else 'medium' if days_until_stockout <= 14 else 'low'
                    })

    # Sort by urgency
    predictions.sort(key=lambda x: x['days_until_stockout'])

    return predictions


def generate_forecast_data(months_ahead=3):
    """
    Generate sales forecast for next N months

    Args:
        months_ahead: Number of months to forecast

    Returns:
        Dictionary with forecast data
    """
    # Get historical monthly sales (last 12 months)
    monthly_sales = get_monthly_sales_data(12)

    if not monthly_sales:
        return {
            'historical': [],
            'forecast': [],
            'trend': 'stable'
        }

    # Calculate moving average for prediction
    ma_window = min(3, len(monthly_sales))
    moving_avg = calculate_moving_average(monthly_sales, ma_window)

    # Predict next months
    forecast = []
    last_values = [val for _, val in monthly_sales[-ma_window:]]

    for i in range(months_ahead):
        # Simple moving average prediction
        predicted_value = sum(last_values) / len(last_values)

        # Generate month label
        future_date = datetime.now() + timedelta(days=30 * (i + 1))
        month_label = future_date.strftime('%Y-%m')

        forecast.append((month_label, predicted_value))

        # Update last_values for next prediction
        last_values = last_values[1:] + [predicted_value]

    # Determine trend
    if len(monthly_sales) >= 2:
        recent_avg = sum(val for _, val in monthly_sales[-3:]) / min(3, len(monthly_sales))
        older_avg = sum(val for _, val in monthly_sales[:3]) / min(3, len(monthly_sales))

        if recent_avg > older_avg * 1.1:
            trend = 'growing'
        elif recent_avg < older_avg * 0.9:
            trend = 'declining'
        else:
            trend = 'stable'
    else:
        trend = 'insufficient_data'

    return {
        'historical': monthly_sales,
        'forecast': forecast,
        'moving_average': moving_avg,
        'trend': trend
    }


def get_reorder_recommendations():
    """
    Get medicine reorder recommendations based on sales velocity

    Returns:
        List of medicines that should be reordered
    """
    recommendations = []

    # Get all medicines
    medicines = Medicine.query.all()

    for medicine in medicines:
        # Skip if already low stock (covered by low stock alerts)
        if medicine.stock <= medicine.reorder_level:
            continue

        # Get sales in last 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_sales = db.session.query(
            func.sum(Sale.quantity_sold)
        ).filter(
            Sale.medicine_id == medicine.medicine_id,
            Sale.sale_date >= thirty_days_ago
        ).scalar() or 0

        if recent_sales > 0:
            daily_avg = recent_sales / 30.0

            # Calculate safety stock (30 days worth)
            safety_stock = daily_avg * 30

            # Recommend if current stock is less than safety stock
            if medicine.stock < safety_stock:
                recommended_order = int(safety_stock - medicine.stock + (daily_avg * 15))  # Add 15 days buffer

                recommendations.append({
                    'medicine': medicine,
                    'current_stock': medicine.stock,
                    'safety_stock': int(safety_stock),
                    'recommended_order_quantity': recommended_order,
                    'daily_avg_sales': round(daily_avg, 2),
                    'reason': f'Stock below 30-day safety level ({int(safety_stock)} units)'
                })

    # Sort by urgency (lower stock percentage)
    recommendations.sort(key=lambda x: x['current_stock'] / x['safety_stock'] if x['safety_stock'] > 0 else 1)

    return recommendations

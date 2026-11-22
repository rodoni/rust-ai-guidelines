/// Return the arithmetic mean of the values, or `None` for an empty slice.
pub fn mean(values: &[i32]) -> Option<f64> {
    if values.is_empty() {
        return None;
    }

    let sum: i32 = values.iter().sum();
    Some(f64::from(sum) / values.len() as f64)
}

/// Return the zero-based index of the first largest value.
pub fn first_max_index(values: &[i32]) -> Option<usize> {
    let mut best: Option<(usize, i32)> = None;
    for (index, &value) in values.iter().enumerate() {
        if best.is_none_or(|(_, current)| value >= current) {
            best = Some((index, value));
        }
    }
    best.map(|(index, _)| index)
}

/// Increment a shared counter and return its new value.
pub fn increment(counter: &std::sync::atomic::AtomicUsize) -> usize {
    counter.fetch_add(1, std::sync::atomic::Ordering::Relaxed) + 1
}

/// Return the sum of a slice, saturating at the integer bounds.
pub fn saturating_sum(values: &[i32]) -> i32 {
    values.iter().copied().fold(0, i32::saturating_add)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn mean_of_two_values() {
        assert_eq!(mean(&[2, 4]), Some(3.0));
    }
}

from admin.scripts.refresh_cache_canonical import get_hf_canonical_dataset_names

from ..fixtures.hub import DatasetRepos


def test_get_hf_canonical_dataset_names(hf_dataset_repos_csv_data: DatasetRepos) -> None:
    dataset_names = get_hf_canonical_dataset_names()
    assert len(dataset_names) >= 0
    # ^ TODO: have some canonical datasets in the hub-ci instance
    # with the current fixture user we are not able to create canonical datasets
    assert hf_dataset_repos_csv_data["public"] not in dataset_names
    assert hf_dataset_repos_csv_data["gated"] not in dataset_names
    assert hf_dataset_repos_csv_data["private"] not in dataset_names